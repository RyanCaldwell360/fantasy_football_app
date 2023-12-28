# Fantasy League Historical Results Viewer

## Project Overview

This project aims to develop a web application that enables members of our fantasy football league to view historical results, including individual game matchups and overall standings, dating back to the 2017 season. 2017 is significant only in that I joined that season. I don't care about the leagure prior to that :smiley:. 


***Data Access***: This project will rely upon the YFPY [package](https://github.com/uberfastman/yfpy) for access to league data through the Yahoo Fantasy API.

***Frontend UI***: This project will rely upon [streamlit.io](https://streamlit.io/), which makes for quick and easy public access for team consumption

***Backend***: To be determined

## Goals

Learn how to build end-to-end system for analytics project. This should be a fun project where I learn a lot! I plan on updating and improving this system over time.

## Project Structure

```
fantasy_football_app/
├── .github/
│   └── workflows/
│       └── ci_cd.yml
├── .streamlit/
│   └── secrets.toml
├── src/
│   ├── backend/
│   │   └── data_extraction/
│   │       ├── backend_config.yml
│   │       └── yahoo_data_script.py
│   └── frontend/
│       └── streamlit_app.py
├── .gitignore
├── requirements.txt
└── README.md
```
## Getting Started

#### Yahoo Fantasy API
This project relies heavily on the [YFPY](https://yfpy.uberfastman.com/index.html) package to access Yahoo fantasy football data. It is a nice python wrapper around the Yahoo API, but requires some setup to access private league's data. The basic process can be followed in 2 steps:

1. Create Yahoo App to generate client id/secret
    1. https://developer.yahoo.com/oauth2/guide/openid_connect/getting_started.html
1. Authenticate using client id/secret
    1. https://developer.yahoo.com/oauth2/guide/flows_authcode/

During the authentication step, you will need to send a response to Yahoo to get an access token that will then be used to request data through YFPY. The following code snippet will return a json object that you can store in a token.json file. That file is then referenced in all YFPY calls.

Here's an example of what a request for the access token could look like:

```python
import os
import requests

# Fetching credentials from environment variables
client_id = os.getenv('YAHOO_CLIENT_ID')
client_secret = os.getenv('YAHOO_CLIENT_SECRET')

url = 'https://api.login.yahoo.com/oauth2/get_token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': 'https://localhost:8080',
    'code': 'xxx',
    'grant_type': 'authorization_code'
}

response = requests.post(url, headers=headers, data=data)
json_response = response.json()
access_token = json_response.get('access_token')
print(json_response)
print(access_token)
```
You can set the 

`os.getenv('YAHOO_CLIENT_ID')`
`os.getenv('YAHOO_CLIENT_SECRET')` 

environment variables from the command line like so:

```bash
export YAHOO_CLIENT_ID="your_client_id_here"
export YAHOO_CLIENT_SECRET="your_client_secret_here"
```

You will need to make sure that you set the 'code' key/value pair to the code that Yahoo provides through your redirect_uri during initial authentication.

Unfortunately, I found that YFPY was throwing OAuth2 errors until I added the "consumer_key", "consumer_secret" and "token_time" to the token.json file. I somewhat figured this out by finding my way to this site while navigating errors: https://pypi.org/project/yahoo-oauth/

#### Streamlit

* Setup streamlit account
* Create new app on [streamlit.io](https://streamlit.io/) website once logged on
    * You will specify this repo to connect to when creating the new app
    * You can specify the streamlit_app.py file within the main branch
* When creating the new app, providing AWS S3 credentials (access key/secret) to the app
    * I created a new user on AWS IAM which has access to S3, and generated new key/secret for streamlit app

## To-Dos

- [ ] create rolling standings by season/week
- [ ] display rolling standings through plot
