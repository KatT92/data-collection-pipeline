FROM python:latest

ENV PYTHONUNBUFFERED 1
# Run bash command 
RUN mkdir /bgg_scraper

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt



# Copy data from docker context
COPY ./scrapers/linkScraper.py /my_app
# Set current working directory
WORKDIR /bgg_scraper

# When we run container this will be the command run
ENTRYPOINT [ "python", "./scrapers/linkScraper.py" ]

# docker run --name my-postgres-container -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 --rm postgres