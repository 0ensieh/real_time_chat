# Sdata_RealTime_Chat

Sdata RealTime Chat is A Django project to chat online with one or more people.


<br>
<h2>How to Run?</h2>
<br>

<h2>
  Create a new virtual environment and activate it.
</h2>

<h3>on Windows:</h3>
<div class="highlight highlight-source-shell">

  ```
  $ pip install virtualenv
  ```
  <br>
  
  ```
  $ virtualenv your_virtualenv_name
  ```
</div>


<h3>on Linux:</h3>
<div class="highlight highlight-source-shell">

  ```
  $ sudo apt-get install python-pip
  ```
  <br>
  
  ```
  $ pip install virtualenv
  ```
  <br>
  
  ```
  $ virtualenv your_virtualenv_name
  ```
</div>

<br>

<h2>
  Set all required environment variables:
</h2>


<br>

<h2>
  Install the dependencies:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ pip install -r requirements.txt
  ```
</div>
<br>

<h2>
  Create and migrate the database:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py migrate
  ```
</div>
<br>

<h2>
  Create a new superuser:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py createsuperuser
  ```
</div>
<br>

<h2>
  Collect static files:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py collectstatic
  ```
</div>
<br>

<h2>
  Run the server on default port 8000:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py runserver
  ```
</div>
<br>

<h2>
  How to get google keys?
</h2>

<ol>
  <li>
    go to this link: <a href="https://console.developers.google.com">Google Developer Console</a>
  </li>

  <li>
    Select your country and confirm the terms and services.
  </li>
  <li>
    Click on Select a new project
  </li>
  <li>
    Click on credentials.
  </li>
  <li>
    Click on “Configure Consent Screen”
  </li>
  <li>
    Select External. Click on create.
  </li>
  <li>
    Enter app name: testapp. Add your support email
  </li>
  <li>
    At the bottom. Add developer contact information. Click on save and continue.
  </li>
  <li>
    Click on save and continue 2 times. Then click on back to the dashboard.
  </li>
  <li>
    Again click on credentials.
  </li>
  <li>
    Click on create credentials. Click on OAuth Client ID.
  </li>
  <li>
    Select Application type as web.
  </li>
  <li>
    Add two Authorized JavaScript origin URLs: http://localhost:8000 and http://127.0.0.1:8000
  </li>
  <li>
    Authorized Redirect URIs: http://localhost:8000/social-auth/complete/google-oauth2/
  </li>
  <li>
    Click on create.
  </li>
  <li>
    If you checked the video then make sure to hit the subscribe button. I make cool Django and react native applications. Your support will be admired. Copy and paste the client id and client secret to your settings.py. 
  </li>
  <li>
    Copy and paste the client id and client secret to your settings.py.

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '##################################'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '###########################'

  </li>

</ol>


<h2>How to get github keys?</h2>
<ol>
  <li>
    You need a GitHub account.
  </li>
  <li>
    Click on your profile. Then click on settings
  </li>
  <li>
    Scroll down and click on developer settings (Left-Hand side)
  </li>
  <li>
    Click on OAuth Apps
  </li>
  <li>
    Click on Register a new application
  </li>
  <li>
    Add application name: test
  </li>
  <li>  
    Homepage URL: http://127.0.0.1:8000
  </li>
  <li>
    Authorization callback URL: http://127.0.0.1:8000/social-auth/complete/github/
  </li>
  <li>
    Click on Register application
  </li>
  <li>
    Generate client secret code.
  </li>
  <li>
    Copy and paste the client id and client secret to your settings.py.

    SOCIAL_AUTH_GITHUB_KEY = '##############################'
    SOCIAL_AUTH_GITHUB_SECRET = '###########################'
  </li>

</ol>

<hr>
<h1>if you want to use accounts app with social-auth-app-django in a separate project</h1>



<h2>What is settings for authentication via google and github in settings.py:</h2>
Add this line to installed apps:

~~~bash  
  INSTALLED_APPS = [
    ...
    ...
    # add this apps for login via google, github and ...
    'social_django',    
]
~~~

Add this lines for authentication backends:

~~~bash  
# add new authentication backend for using django all-auth package
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2', # for google
    'social_core.backends.github.GithubOAuth2', # for github
    'django.contrib.auth.backends.ModelBackend' # for normal authentication
]

~~~


Add this middleware:

~~~bash  
MIDDLEWARE = [
    ...
    ...
    'social_django.middleware.SocialAuthExceptionMiddleware', #add this middleware for login via social accounts
]

~~~


Add this context processor:

~~~bash  

TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                ...
                'social_django.context_processors.backends', #add this context processor for login via social accounts
            ],
        },
    },
]

~~~


<h2>and the keys: </h2>

~~~bash

# key and secret for google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'XXXXXXXXXXXXXXXXXXXXX'

# key and secret for github
SOCIAL_AUTH_GITHUB_KEY = 'XXXXXXXXXXXXXXXXXXXX'
SOCIAL_AUTH_GITHUB_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXX'

~~~