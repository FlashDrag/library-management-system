# Library Management System

[Live link](#)

[SpreadSheet](#)

This is a python script that uses the gspread library to access a Google Spreadsheet and perform operations on it.

## Features


## Prerequisites
To run this script, you need to have the following installed:

- Python 3.x
- gspread library
- Google API credentials (in form of a JSON file)

## How to run
- Clone this repository to your local machine
- Replace the credentials JSON file with your own Google API credentials;

    [See instruction](instruction.md)
- Run the script by executing python run.py in the terminal

## Creating the Heroku app

1. When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:
    1. `heroku/python`
    2. `heroku/nodejs`

2. Config Vars
- Create a _Config Var_ called `PORT`. Set this to `8000`
- Create another _Config Var_ called `CREDS` and paste the JSON credentials into the value field.

3. Connect your GitHub repository and deploy as normal.

## Libraries used
- gspread: This is a Python library used to access and manage Google Spreadsheets.

- Google OAuth2 client: This is used to authenticate the application and grant it access to the Google APIs.


## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.
