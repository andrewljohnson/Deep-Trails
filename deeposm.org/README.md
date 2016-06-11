# DeepOSM.org

A website to browse OpenStreetMap errors detected by DeepOSM.

## Run the Site Locally

This development setup for Django/postgres/docker setup is based on the [stock Docker Compose docs for Django/Postgres](https://docs.docker.com/compose/django/). 

Start Docker Quickstart Terminal on a Mac. Then:

    cd /PATH_TO_REPO/deeposm.org
    docker-compose up

Then, the site is live at your docker IP, similar to: http://192.168.99.100:8000/

## Running Migrations via Docker Compose

[Per these docs](https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/):

    docker-compose run web /usr/local/bin/python manage.py migrate


## Deploy to Amazon Elastic Beanstalk (EBS)

Follow [this tutorial](https://realpython.com/blog/python/deploying-a-django-app-and-postgresql-to-aws-elastic-beanstalk/). It goes like:

Use the EBS command line tools to deploy:

    pip install awsebcli

Per tutorial, run

    eb create
    eb config

Per tutorial, if you search for the terms ‘WSGI’ in the file, and you should find a configuration section to change application.py to:

    website/wsgi.py
   
Then:

    eb deploy

Also, set your AWS credentials on EB:

    eb setenv AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
    eb setenv AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

## Data Displayed

The production findings are created and posted to S3 by running these commands, using DeepOSM. 

For Delaware:

    python bin/create_training_data.py --number-of-naips=-1
    python bin/train_neural_net.py --number-of-epochs=4 --neural-net=one_layer_relu_conv --post-findings-to-s3

For Maine:

    python bin/create_training_data.py --number-of-naips=175 --naip-path 'me' 2013 --label-data-files 'http://download.geofabrik.de/north-america/us/maine-latest.osm.pbf'
    python bin/train_neural_net.py --number-of-epochs=4 --neural-net=one_layer_relu_conv --post-findings-to-s3
