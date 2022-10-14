# Data collection pipeline
This project scrapes data from a popular board game website. It includes input for a user to decide how many items they want to scrape.
It can save the data and images locally, and upload the data to AWS RDS and save the images to aws S3 buckets depending on personal preference.

## Scrapers
These scrape links from the website using seleniums chrome webdriver.

### linkScraper.py
It gets the xpath correpsonding to the link on the list.
To run in terminal type:
'''python linkScraper.py'''
This will prompt the user to type in a minimum and maximum number, corresponding to the board game rank they want to scrape. It will scrape all the links between and including these values.
It saves the data to a file called 'bg_links.py' in the form of a list
This takes the 'url' from config.py in the environment variables and will not run without it.

### pageScraper.py
This takes all the links saved in 'bg_links.py' and scrapes each one using seleniums chrome webdriver.
It gets data using XPATH including:
url, game name, images, rank names, rank numbers, min players, max players, min time, max time and designer.
It also adds a unique id from the website, as well as a generated uuid.
To run in terminal type:
'''python pageScraper.py'''
This will prompt the user to decide whether they want to save the files locally or upload to AWS S3 and RDS.
The data is saved locally in json format in a file called 'raw_data/<id>/data.json' and up to 5 images are stored in a folder called 'raw_data/<id>/images' in the format '<id>_<i>.jpg' where i is between 0 and 4.
To upload to AWS, it requires the user to have access to the data required in the 'connect.py' file, such as the AWS endpoint, username and password.

## config.py and .env
The config files connect the the private .env files and contain the url, db, username, password and endpoint using 'the 'decouple' library.
The information from the .env file is needed to run most of files in this repository.

## connect.py
This connects to AWS using SQLalchemy to create an engine.
It requires data from a private .env file whic includes the AWS endpoint, username and password.

## SQL
The tables on AWS RDS were created using postgreSQL, they take the data collected from 'pageScraper.py' and upload them to AWS RDS.
### createTable.py, deleteTable.py, readTable.py
The createTable.py file was used to create the tables.
The readTable.py file is used to read tables, and is used to stop the duplication of data.
The deleteTable.py fle is used to drop all tables in the database.


## Tests
These tests are run using the 'unittest' module.

### unit tests
testing linkScraper.py
testing pageScraper.py

### integration tests
The integration first runs the linkScraper.py file to get the links, and gets the first link from the page. It then runs the pageScraper.py file to get data from the page associated with that link. The expected result should be 'Gloomhaven'.
Note: Tis file may need to be changed if the rank order changes.


## Large-scale scraping and preventing rescraping
I ran the scrapers for large amounts (>100) of data to find and fix errors. These included data that used different xpaths on each page, different information given for the same xpath and problems turning pages. In order to combat this I added try/except statements where necessary and used more specific xpath, as well as adding a page turning function.
To prevent rescraping, for each link on 'pageScraper.py', it checks if the data is already saved where the user wants it to be saved (locally or on AWS RDS using an SQL request). If it is not saved, it then runs the scraper, if it isn't it goes on to the next link.
Note: As the data on each page isn't static, this could mean data on the database can become out of data, each set of data is associated with the time it was uploaded.


 > Everything after this point is under construction

## AWS
### S3
> boto3
> buckets
### RDS
> SQLalchemy, connect.py,  .env
> SQL tables
> security groups
> IAM

## Docker
### Headless Mode

### Docker images
> Python, selenium, prometheus, grafana

> docker-compose.yml, Dockerfile, requirements.txt, .dockerignore
'''docker run --name my-postgres-container -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USERNAME=mysecretusername -e AWS_ENDPOINT=awsendpoint -d -p 5432:5432 --rm postgres'''

### Docker volumes
> bg_links.py
### Dockerhub


## AWS EC2 instances


## Prometheus
> Monitoring, metrics, prometheus.yml
> Running in a docker container
> promQL

## Grafana
After running grafana in a docker container 
'''docker run -d --name=grafana -p 3000:3000 grafana/grafana-enterprise''', you can enter login details by going to 'localhost:3000', initially using 'admin' as username as password before being prompted to give a new password.
We can add prometheus as a data source using '''host.docker.internal:9090''' as we are running prometheus in a docker container.
> Docker metrics
> OS metrics

## Github
> .gitignore

### Github secrets
### Github actions



## versions
> python 3.10
> prettier, .prettierignore