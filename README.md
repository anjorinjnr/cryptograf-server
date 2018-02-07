# cryptograf-server

### Getting Setup

0. Install SDK for App Engine 
Follow the instructions [here](https://cloud.google.com/appengine/docs/standard/python/download) 

1. Download source code
https://github.com/anjorinjnr/cryptograf-server

2. Install dependencies 

`pip install -t lib -r requirements.txt`

3. Start Server

`dev_appserver.py app.yaml`


#### Testing
To run unit test

`python runner.py <path-to-sdk>`


### References

1. Webapp2 Framework: 
http://webapp2.readthedocs.io/en/latest/index.html

2. GAE Python:
https://cloud.google.com/appengine/docs/standard/python/

3. Cerberus for Data Validation
http://docs.python-cerberus.org/en/stable/usage.html

4. Python Style Guide
https://google.github.io/styleguide/pyguide.html#Classes
