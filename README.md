## flasky-appengine [![Build Status](https://travis-ci.org/russomi/flasky-appengine.svg?branch=master)](https://travis-ci.org/russomi/flasky-appengine) [![Coverage Status](https://coveralls.io/repos/russomi/flasky-appengine/badge.svg)](https://coveralls.io/r/russomi/flasky-appengine)

flasky + appengine FTW!

This repo is based on the excellent [flasky](https://github.com/miguelgrinberg/flasky) project.  It has been modified to be compatible with Google App Engine.

## Prerequisites

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/), including the [gcloud tool](https://cloud.google.com/sdk/gcloud/), and [gcloud app component](https://cloud.google.com/sdk/gcloud-app).
1. Install [MySQL](http://dev.mysql.com/downloads/)
1. Install virtualenvwrapper ```pip install virtualenvwrapper``` 
1. [Sign up](http://cloud.google.com/console) for a Google Cloud Platform project, and
set up a Cloud SQL instance, as described [here](https://developers.google.com/cloud-sql/docs/instances), and a
Cloud Storage bucket, as described [here](https://developers.google.com/storage/docs/signup). You'll want to configure
your Cloud SQL instance in the config.py. To keep costs down, we suggest signing up for a D0 instance with package billing. 
1. Visit your project in the
[Google Cloud Console](http://cloud.google.com/console), going to the App Engine section's **Application Settings**
area, and make a note of the **Service Account Name** for your application, which has an e-mail address
(e.g. `<PROJECT_ID>@appspot.gserviceaccount.com`). Then, visit the Cloud Storage section of your project,
select the checkbox next to the bucket you created in step 3, click
**Bucket Permissions**, and add your Service Account Name as a **User** account that has **Writer** permission.

## Run Locally
1. Setup the gcloud tool.

   ```
   gcloud components update app
   gcloud auth login
   gcloud config set project <your-app-id>
   ```
   You don't need a valid app-id to run locally, but will need a valid id to deploy below.
   
1. Clone this repo.

   ```
   git clone https://github.com/russomi/flasky-appengine.git
   ```
   
1. Create a virtual environment

    ```
    mkvirtualenv flasky-appengine
    ```
    
1. Install requirements.txt

    ```
    pip install -r requirements/dev.txt
    pip install -t lib -r requirements/common.txt
    ```

    Tip:
    - If the library is provided by the google app engine environment, ```pip install``` into the virtualenv.
    - If the library is not provided by the google app engine environment, ```pip install -t lib``` directory.

1. Add google_appengine sdk and lib folder to the virtualenv:

    ```
    add2virtualenv lib
    add2virtualenv ~/google-cloud-sdk/platform/google_appengine
    ```
       
1. Run this project locally from the command line.

   ```
   gcloud preview app run flasky-appengine/
   ```

1. Visit the application at [http://localhost:8080](http://localhost:8080).

## Deploying

1. Use the [Cloud Developer Console](https://console.developer.google.com)  to create a project/app id. (App id and project id are identical)
2. Configure gcloud with your app id.

   ```
   gcloud config set project <your-app-id>
   ```
1. Use the [Admin Console](https://appengine.google.com) to view data, queues, and other App Engine specific administration tasks.
1. Use gcloud to deploy your app.

   ```
   gcloud preview app deploy flasky-appengine/
   ```

1. Congratulations!  Your application is now live at your-app-id.appspot.com

## Contributing changes

* See [CONTRIBUTING.md](CONTRIBUTING.md)

## Licensing

* See [LICENSE](LICENSE)