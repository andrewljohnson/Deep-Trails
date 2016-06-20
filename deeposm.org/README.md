# DeepOSM.org

A website to browse OpenStreetMap errors detected by DeepOSM.

## Run the Site Locally

This development setup for Django/postgres/docker setup is based on the [stock Docker Compose docs for Django/Postgres](https://docs.docker.com/compose/django/). 

Start Docker Quickstart Terminal on a Mac. Then:

    cd /PATH_TO_REPO/deeposm.org
    docker-compose up

Then, the site is live at your docker IP, similar to: http://192.168.99.100:8000/

## Running Migrations via Docker Compose

    docker-compose run web /usr/local/bin/python manage.py migrate  --run-syncdb

## Server Setup

Started with this cookiecutter: https://github.com/dolphinkiss/cookiecutter-django-aws-eb

    cookiecutter https://github.com/dolphinkiss/cookiecutter-django-aws-eb

Chose this config:

    aws_eb_type [python/docker]: docker
    project_name [myproject]: error_browser
    django_version [1.9.1]: 
    setup_local_env [yes]: 
    virtualenv_bin [virtualenv]: 
    source_root [.]: error_browser

Chose these settings for eb init:

    eb init

	Select a default region
	3) us-west-2 : US West (Oregon)

	Select an application to use
	3) [ Create new Application ]

	Enter Application Name: error_browser

	It appears you are using Docker. Is this correct?
	(y/n): y

	Select a platform version.
	1) Docker 1.9.1

	Do you want to set up SSH for your instances?
	(y/n): y

	Select a keypair.
	1) deeposm-andrew
	(default is 2): 1


## Creating Production Findings

The production findings are created and posted to S3 by running these commands, using DeepOSM. 

For Delaware:

    python bin/create_training_data.py --number-of-naips=-1
    python bin/train_neural_net.py --number-of-epochs=4 --neural-net=one_layer_relu_conv --post-findings-to-s3

For Maine:

    python bin/create_training_data.py --number-of-naips=175 --naip-path 'me' 2013 --label-data-files 'http://download.geofabrik.de/north-america/us/maine-latest.osm.pbf'
    python bin/train_neural_net.py --number-of-epochs=4 --neural-net=one_layer_relu_conv --post-findings-to-s3
