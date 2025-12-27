#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define the application name and the environment
APP_NAME="your-app-name"
HEROKU_API_KEY="your-heroku-api-key"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null
then
    echo "Heroku CLI could not be found. Please install it to proceed."
    exit 1
fi

# Login to Heroku
echo "Logging into Heroku..."
echo $HEROKU_API_KEY | heroku auth:token

# Create a new Heroku app if it doesn't exist
if ! heroku apps:info -a $APP_NAME &> /dev/null
then
    echo "Creating Heroku app..."
    heroku create $APP_NAME
fi

# Set the buildpacks for Python and Node.js
echo "Setting buildpacks..."
heroku buildpacks:set heroku/python -a $APP_NAME
heroku buildpacks:add --index 1 heroku/nodejs -a $APP_NAME

# Push the code to Heroku
echo "Deploying to Heroku..."
git push heroku main

# Run database migrations if necessary
# Uncomment the following line if you have migrations to run
# heroku run python manage.py migrate -a $APP_NAME

# Open the app in the default web browser
echo "Opening the app in your browser..."
heroku open -a $APP_NAME

echo "Deployment completed successfully!"