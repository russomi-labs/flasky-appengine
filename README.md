Flasky
======

This repository contains the source code examples for my O'Reilly book [Flask Web Development](http://www.flaskbook.com).

The commits and tags in this repository were carefully created to match the sequence in which concepts are presented in the book. Please read the section titled "How to Work with the Example Code" in the book's preface for instructions.

## Changes to support Google App Engine

- Added new configuration option MAIL_USE_GAE to support sending email via Google App Engine api vs. Flask-Mail.
- Added _send_email_gae() to support sending emails from Google App Engine
- Added SERVER_NAME to testing config to support running tests in PyCharm
- Added MySQLdb support since running under Google App Engine dev server does not support importing sqlite
- Added appengine_config.py to support vendoring
- Add the following paramters when running dev_appserver.py to send email when running locally
    ```
    --smtp_host=smtp.googlemail.com --smtp_port=587 --smtp_user=<enter gmail address> --smtp_password=<enter password>
    ```

## TODO

- [x] Move create_app() from manage.py into a main.py
- [ ] Refactor GAE specific config into subclass of ProductionConfig
- [ ] Update manage.py to support deploying to Google App Engine and doing DB migrations
- [ ] Update manage.py to run under Google App Engine dev environment
- [ ] Relocate venv to outside of project root to avoid deploying it to GAE
- [ ] Take a look at this script... https://github.com/anler/App-Engine-runserver.py/blob/master/runserver.py
- [ ] Relocate venv to avoid deploying to App Engine
- [ ] Add instructions on how to install mysql locally