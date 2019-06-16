# Weather App
This app shows current and forecasted weather for a zip code entered by a user.

Live version of this app can be seen here: https://fn-weather-app.herokuapp.com/.

Built using Django, and deployed with Heroku.

## Getting it to work
This app uses the OpenWeatherMap API, so you would need to generate an API key.

You can get that API key by signing up at: https://openweathermap.org/api.

Also, ensure to have everything installed that is shown in the ```requirements.txt``` file. 
      
1. Local
    - Update the ```API_KEY``` variable in the ```views.py``` file to reflect your new key
    - Make the following changes in the ```settings.py``` file:
      - Change the enviornment variables of ```SECRET_KEY``` and ```DEBUG``` to your hard coded values or create your own enviornment variables for them
      - ```ALLOWED_HOSTS``` can be empty when ```DEBUG=True``` and only needed if you deploy the site, in which case you would be replacing the value anyways
    
2. Deployed
    - First steps would be the same as described above in the Local instructions
      - You want ```DEBUG=False``` in production
    - Include the deployment url in the ```ALLOWED_HOSTS```
    - You would then need to run the following command to ensure the static files are available in production
        ```
        python manage.py collectstatic
        ```
    - The previous step should generate a ```staticfiles``` directory, if it doesn't you may want to create the folder then run the command again
    - If you run into the following error when deploying to Heroku
        ```
        Error while running '$ python manage.py collectstatic --noinput'.
        ```
    - Run the following Heroku command, then try pushing the code again
        ```
        heroku config:set DISABLE_COLLECTSTATIC=1
        ```
    - After you deploy the app you can change this in your app settings from 1 to 0 to ensure collectstatic runs in future deployments
