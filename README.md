# Library Management System

[App link](https://library-management-system.herokuapp.com/)

[SpreadSheet](https://docs.google.com/spreadsheets/d/1guVUVRVMsu2nebKllN6_58nDraMnEftIoTaRtlUnRME/edit?usp=sharing)

[Library Management System](https://library-management-system.herokuapp.com/) is a Python CLI application that uses the gspread library to access a Google Spreadsheet and perform operations on it. The app idea is to create a library management system that allows the librarian to add, remove, check out and return books. The app is built using the MVC model and the Pydantic library for data validation.


![Responsive Mockup](docs/supp-images/responsive-mockup.png)

## Table of Contents
- [**User Experience UX**](#user-experience-ux)
  - [User Stories](#user-stories)
  - [Structure](#structure)
  - [Flowchart](#flowchart)
- [**Features**](#features)
    - [Main menu](#main-menu)
    - [Add book](#add-book)
    - [Remove book](#remove-book)
    - [Check out book](#check-out-book)
    - [Return book](#return-book)
  - [MVC Model](#mvc-model)
  - []()
  - []()
  - []()
  - []()

- [**Technologies Used**](#technologies-used)
- [**Testing**](#testing)
- [**Deployment**](#deployment)
- [**Credits**](#credits)

## User Experience (UX)

### User Stories
- #### Librarian
    ...

- #### Frequent user goals
  - ...

[Back to top](#table-of-contents)


### Structure

...

[Back to top](#table-of-contents)


### Flowchart
![Flowchart](docs/supp-images/flowchart.png)

## Features
- #### Main menu

- #### Add book

- #### Remove book

- #### Check out book

- #### Return book

### MVC Model

### API Integration

### Type Hints

### Pydantic Validation

### Enum, TypedDict

### Tabulate


[Back to top](#table-of-contents)

## Technologies Used
- [Python](#) - building the app
- [VSCode](#) - IDE
- [GitHub]() - ...
- [GIT]() - ...
- [Heroku]() - ...
- [Google Spreadsheets API]() - ...
- []() - ...
- []() - ...
- []() - ...
- []() - ...
- []() - ...
- []() - ...

### Dependencies
- [Pytest]() - ...
- [datetime]() - ...
- [Pydantic]() - ...
- [gspread]() - Python library used to access and manage Google Spreadsheets.
- [flake8]() - ...
- [logtail]() - ...
- [mypy]() - ...
- [tabulate]() - ...
- [Google OAuth2 client]() - authenticate the application and grant it access to the Google APIs.
- []() - ...

[Back to top](#table-of-contents)

## Testing
See [TESTING.md](https://github.com/FlashDrag/library-management-system/blob/main/docs/testing.md) for an overview of the game testing and debugging.

[Back to top](#table-of-contents)


## Deployment
The App link is https://library-management-system.herokuapp.com/

The app is hosted on [Heroku]()

#### How to connect to Google Spreadsheet API and get creadentials

[Here you can find instructions](https://github.com/FlashDrag/love-sandwiches/blob/main/docs/instruction.md)

#### To run the game on a local machine:
To run this script, you need to have the following installed:
- Python 3.x
- gspread library
- Google API credentials (in form of a JSON file)
To run:
- Clone this repository to your local machine
- Replace the credentials JSON file with your own Google API credentials;
- Run the script by executing python run.py in the terminal

#### To deploy the project:

- ##### Creating the Heroku app
1. When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:
    1. `heroku/python`
    2. `heroku/nodejs`

2. Config Vars
- Create a _Config Var_ called `PORT`. Set this to `8000`
- Create another _Config Var_ called `CREDS` and paste the JSON credentials into the value field.

3. Connect your GitHub repository and deploy as normal.

----
- Fork or clone this repository.
- Log into your account on Heroku.
- Create a new Heroku app.
- Navigate to Settings tab.
- Set up environmental variables in config vars section. In this case, it's CREDS(credentials of Google service account) and PORT(value 8000).
- Set the buildbacks to python and NodeJS in that order.
- Configure GitHub integration, choose main branch in the Deploy tab.
- Click Deploy branch.
----
[Back to top](#table-of-contents)

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

[Back to top](#table-of-contents)

## Credits
### Code
The [Library Management System](https://library-management-system.herokuapp.com/) programm based on my own implementation of code, applying what I've learned from [CodeInstitute Full Stack Developer Course](https://codeinstitute.net/ie/full-stack-software-development-diploma/) and other tutorials.

### Content
...

[Back to top](#table-of-contents)