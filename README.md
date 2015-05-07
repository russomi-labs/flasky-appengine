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
