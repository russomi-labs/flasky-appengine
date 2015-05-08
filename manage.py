#!/usr/bin/env python
import os

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from main import app
from app import db
from app.models import User, Follow, Role, Permission, Post, Comment
from flask.ext.script import Manager, Shell, Command, Option
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys

        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware

    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

    # create self-follows for all users
    User.add_self_follows()


@manager.command
def hello(name="Fred"):
    """
    Example command with named arg

    > python manage.py hello --name=Joe
    hello Joe

    or

    > python manage.py hello -n Joe
    hello Joe

    :param name: Who to say hello to
    """
    print "hello", name


class Dev_appserver(Command):
    option_list = (
        Option('-y', '--yaml_path', dest='yaml_path', default='.'),
        Option('-l', '--log_level', dest='log_level', default='debug'),
        Option('-a', '--allow_skipped_files', dest='allow_skipped_files', default=True),
        Option('-d', '--data_storage_path', dest='data_storage_path', default='.appengine_data'),
        Option('-smtp_host', '--smtp_host', dest='smtp_host', default='smtp.googlemail.com'),
        Option('-smtp_port', '--smtp_port', dest='smtp_port', default=587),
        Option('-smtp_user', '--smtp_user', dest='smtp_user', default=os.environ.get('MAIL_USERNAME')),
        Option('-smtp_password', '--smtp_password', dest='smtp_password', default=os.environ.get('MAIL_PASSWORD')),
        Option('-smtp_allow_tls', '--smtp_allow_tls', dest='smtp_allow_tls', default=True),
    )

    def run(self, yaml_path, log_level, allow_skipped_files, data_storage_path, smtp_host, smtp_port, smtp_user,
            smtp_password, smtp_allow_tls):
        """
        Run the Google App Engine dev_appserver.py with defaults
        """
        from subprocess import call

        cmd = ['dev_appserver.py',
               '--log_level={}'.format(log_level),
               '--storage_path={}'.format(data_storage_path),
               '--allow_skipped_files={}'.format(allow_skipped_files),
               '--smtp_host={}'.format(smtp_host),
               '--smtp_port={}'.format(smtp_port),
               '--smtp_user={}'.format(smtp_user),
               '--smtp_password={}'.format(smtp_password),
               '--smtp_allow_tls={}'.format(smtp_allow_tls),
               yaml_path]

        # execute the command
        call(cmd)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('dev_appserver', Dev_appserver)

if __name__ == '__main__':
    manager.run()
