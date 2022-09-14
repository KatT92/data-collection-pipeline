import requests2
# Change this with your URL
url = 'https://bggdata.s3.eu-west-2.amazonaws.com/161936_0.jpg'

response = requests2.get(url)
with open('161936_0.jpg', 'wb') as f:
    f.write(response.content)


# creates file in same working directory
# file name can't be named requests due to circular import
