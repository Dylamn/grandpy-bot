# Grandpy Bot
[comment]: <> (Badges)
[![Build Status](https://travis-ci.com/Dylamn/grandpy-bot.svg?branch=master)](https://travis-ci.com/Dylamn/grandpy-bot)
[![codecov](https://codecov.io/gh/Dylamn/grandpy-bot/branch/develop/graph/badge.svg?token=P2LSFZLB2S)](https://codecov.io/gh/Dylamn/grandpy-bot)

## Installation
Copy the ``.env.example`` file at the root of the project and rename it ``.env``.
Fill the variable on your need.

Then, in order to run the application, you must install its dependencies which are
listed in the ``requirements.txt`` file with pip:
````shell
$ pip install -r requirements.txt
````

### Virtual Environments
Sometimes you want to keep libraries from polluting system installs 
or use a different version of libraries than the ones installed on the system.  
For this purpose, the standard library as of Python 3.3 comes with the "venv" 
module in order to help maintain these separate versions.
These are others libraries which do the same but here we'll keep with the standard.

For a more in-depth tutorial, 
check the [Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html) documentation.

So, lets create our virtual environment:
1. Go to the ``grandpy-bot`` project directory:
    ```shell
    $ cd path/to/grandpy-bot
    ```
2. Create your virtual environment:
    ```shell
    $ python3 -m venv my_venv
    ```
3. Activate your virtual environment:
    ```shell
    $ source my_venv/bin/activate
    ```
    On Windows it will be a little different:
    ```shell
    $ my_venv\Scripts\activate.bat
    ```
   > If you use Powershell, the file to use is ``activate.ps1`` instead.

You now have finished setting up your virtual environment.

> To exit the virtual environment, simply type the command ``deactivate``

### Build the CSS
The project uses [Tailwindcss](https://tailwindcss.com/) and requires you to build the `.css` file in order
to get the styles for the front-end of the project.

Use ``npm run build`` which will build the ``styles.css`` file.

#### Building for production
When building for **production**, 
set ``NODE_ENV=production`` on the command line when building your CSS:
````shell
$ NODE_ENV=production npm run build
````
This will make sure Tailwind removes any unused CSS for best performance.

### Run on localhost
After the installation steps, you can run the application through the terminal with the following command (don't 
forget to activate your virtual environment):
```shell
$ flask run
```
or with [Gunicorn](https://gunicorn.org/):
````shell
$ gunicorn wsgi:app
````
