# Fantasy League Historical Results Viewer

## Project Overview

This project aims to develop a web application that enables members of our fantasy football league to view historical results, including individual game matchups and overall standings, dating back to the 2020 season. The application will leverage Python, the YFPY package, and web development technologies to fetch, process, and display data in an interactive and user-friendly manner.

## Goals

- **Data Retrieval**: Fetch historical matchup and standings data from the Yahoo Fantasy Sports API.
- **Data Presentation**: Display individual game matchups and overall standings for each season since 2020, including playoff results.
- **User Interface**: Develop an intuitive and engaging user interface for league members to interact with the data.
- **Scalability and Performance**: Ensure the application can handle growing data and user base efficiently.

## Project Structure

```
fantasy_football_app/
├── .github/
│ └── workflows/
│ └── ci_cd.yml
├── src/
│ ├── backend/
│ │ └── (Python backend files)
│ └── frontend/
│ └── (HTML, CSS, JavaScript files)
├── docs/
│ └── (Documentation and resources)
├── tests/
│ └── (Unit and integration tests)
├── .gitignore
├── requirements.txt
└── README.md
```
## Getting Started

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

## To-Dos

- [x] Yahoo developer setup: https://developer.yahoo.com/oauth2/guide/flows_authcode/
- [ ] Implement basic functionality to fetch data from Yahoo Fantasy API.
- [ ] Process and format the fetched data for web display.
- [ ] Set up a basic web server (Flask/Django) for backend API.
- [ ] Design a preliminary frontend interface.
- [ ] Test data fetching and processing modules.
- [ ] Deploy a prototype version for user feedback.