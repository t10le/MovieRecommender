# Movie Recommender Interface Setup

This system was built using Python Flask as the web server and React.js as the front end interface. 

## Cloning From GitHub

Copy the github repository's URL, then navigate to a terminal on your local machine and enter the following commands:

```
 git clone <repo-url>
 cd MovieRecommender/
```

## Installing Dependencies

React requires npm packages to be able to function correctly, these packages can be installed as followed:

```
 cd client/
 npm install
```

Python has packages required to run as well such as Flask, however the folder /server/venv has all the packages required for the environment to function correctly.

## Running the Program

The system's python based API can be started from the client directory as follows:

```
 npm run start-api
```

Then open a new terminal and navigate to the MovieRecommender directory then execute the following commands to start the interface:

```
 cd client/
 npm start
```
