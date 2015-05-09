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

## Setup

### Prerequisites

1. Install the Google App Engine SDK
2. Install [MySQL](http://dev.mysql.com/downloads/)
3. [Sign up](http://cloud.google.com/console) for a Google Cloud Platform project, and
set up a Cloud SQL instance, as described [here](https://developers.google.com/cloud-sql/docs/instances), and a
Cloud Storage bucket, as described [here](https://developers.google.com/storage/docs/signup). You'll want to name
your Cloud SQL instance "wordpress" to match the config files provided here. To keep costs down, we suggest signing up for a D0 instance with package billing. 
4. Visit your project in the
[Google Cloud Console](http://cloud.google.com/console), going to the App Engine section's **Application Settings**
area, and make a note of the **Service Account Name** for your application, which has an e-mail address
(e.g. `<PROJECT_ID>@appspot.gserviceaccount.com`). Then, visit the Cloud Storage section of your project,
select the checkbox next to the bucket you created in step 3, click
**Bucket Permissions**, and add your Service Account Name as a **User** account that has **Writer** permission.

### Cloning and setup

#### Step 1: Clone
Clone this git repo and its submodules by running the following commands:

    $ git clone https://github.com/russomi/flasky.git
    $ cd flasky/

#### Step 2: Create virtualenv
Create the virtualenv:

    $ virtualenv venv
    $ source venv/bin/activate
    
#### Step 3: Install requirements
Install requirements into local lib folder:

    $ pip install -t lib -r requirements/dev.txt

#### Step 4: Add `lib` directory to virtualenv
Add lib folder to the virtualenv:

    $ add2virtualenv lib

#### Step 5: 
Add google_appengine sdk and lib folder to the virtualenv:

    $ add2virtualenv lib
    $ add2virtualenv ~/google-cloud-sdk/platform/google_appengine








## Running locally

>First, edit [wp-config.php](https://github.com/GoogleCloudPlatform/appengine-php-wordpress-starter-project/edit/master/wp-config.php)
  so that the local environment password for root is not literally the string "password" -- unless that's what you used
  when setting up MySQL locally.

Using MySQL's command line version, run `databasesetup.sql` to set up your local database. For a default installation (no root password)
this would be:

    mysql -u root < databasesetup.sql

But really, all it's doing is running this line -- the WordPress installation script will do the heavy lifting
when it comes to setting up your database.

    CREATE DATABASE IF NOT EXISTS wordpress_db;

To run WordPress locally on Windows and OS X, you can use the
[Launcher](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_PHP)
by going to **File > Add Existing Project** or you can run one of the commands below.

On Mac and Windows, the default is to use the PHP binaries bundled with the SDK:

    $ APP_ENGINE_SDK_PATH/dev_appserver.py path_to_this_directory

On Linux, or to use your own PHP binaries, use:

    $ APP_ENGINE_SDK_PATH/dev_appserver.py --php_executable_path=PHP_CGI_EXECUTABLE_PATH path_to_this_directory

Now, with App Engine running locally, visit `http://localhost:8080/wp-admin/install.php` in your browser and run
the setup process, changing the port number from 8080 if you aren't using the default.
Or, to install directly from the local root URL, define `WP_SITEURL` in your `wp-config.php`, e.g.:

    define( 'WP_SITEURL', 'http://localhost:8080/');

You should be able to log in, and confirm that your app is ready to deploy.

### Deploy!

If all looks good, you can upload your application using the Launcher or by using this command:

    $ APP_ENGINE_SDK_PATH/appcfg.py update APPLICATION_DIRECTORY

Just like you had to do with the local database, you'll need to set up the Cloud SQL instance. The SDK includes
a tool for doing just that:

    google_sql.py <PROJECT_ID>:wordpress

This launches a browser window that authorizes the `google_sql.py` tool to connect to your Cloud SQL instance.
After clicking **Accept**, you can return to the command prompt, which has entered into the SQL command tool
and is now connected to your instance. Next to `sql>`, enter this command:

    CREATE DATABASE IF NOT EXISTS wordpress_db;

You should see that it inserted 1 row of data creating the database. You can now type `exit` -- we're done here.

Now, just like you did when WordPress was running locally, you'll need to run the install script by visiting:

    http://<PROJECT_ID>.appspot.com/wp-admin/install.php

Or, to install directly from the root URL, you can define WP_SITEURL in your `wp-config.php`, e.g.:

    define( 'WP_SITEURL', 'http://<YOUR_PROJECT_ID>.appspot.com/');


## TODO

- [x] Move create_app() from manage.py into a main.py
- [x] Update manage.py to run under Google App Engine dev environment
- [x] Relocate venv to outside of project root to avoid deploying it to GAE
- [ ] Refactor GAE specific config into subclass of ProductionConfig
- [ ] Update manage.py to support deploying to Google App Engine and doing DB migrations
- [ ] Take a look at this script... https://github.com/anler/App-Engine-runserver.py/blob/master/runserver.py
- [ ] Add instructions on how to install mysql locally
