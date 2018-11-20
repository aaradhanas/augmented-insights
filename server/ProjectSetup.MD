### PYTHON INSTALLATION

1. Install the latest version of python from https://www.python.org/downloads/
2. Set the environment variable PYTHONPATH to the Python installation location (<INSTALL_DIR>/python)
3. Add PYTHONPATH to Path variable under system variables
4. Close any existing command prompts.
5. Open a new command prompt and type 'python'. You should see the python console.

### PIP INSTALLATION

Pip is a package management system used to install and manage software packages written in Python.

1. Save the content of https://bootstrap.pypa.io/get-pip.py to a file (say, get-pip.py).
2. Run 'python get_pip.py' to install pip.
3. You will find it installed under <INSTALL_DIR>/python/Scripts.
4. Add this path to Path variable under system variables

**How to track the dependencies installed via pip?**

`pip freeze > requirements.txt`

**How to install the dependencies?**

`pip install -r requirements.txt`

### PIPENV INSTALLATION

Pipenv is a packaging tool for Python that solves some common problems associated with the typical workflow using pip, virtualenv, and the good old requirements.txt. If you are aware of the node package manager (npm), this is very similar to it.

1. Install pipenv using the command - `pip install pipenv`
2. Navigate to your project working directory
3. For example, lets assume you would like to install the pandas library.
4. Run `pipenv install pandas`
5. You will see that a new folder is created under 'C:\Users\<USERNAME>\.virtualenvs'. The name of the directory is derived from the directory in which this command was executed and the hashed value of its absolute path. So, if you change the directory location (or) name, make sure to run `pipenv install` to create a new virtual environment and install dependencies.

  This directory is called a **virtual environment**. This is useful when there are multiple python projects which require differnt versions of a dependency. This mechanism helps in isolation of the projects.

6. You will also see that a file called **Pipfile** is created under your project directory. This file holds information about the packages that you have installed using the pipenv install command. Once this file is created, you will see that the package you chose to install gets installed (in our case, pandas).

7. Then, you will find a file called **Pipfile.lock** under your project directory. This file contains information about the exact version of the installed package and the dependencies of the package we installed. For pandas, the dependent packages are numpy, python-dateutil, pytz, etc.

  This file helps in avoiding the risks of automatically upgrading packages that depend upon each other and breaking your project dependency tree.

8. To view the dependency tree of the project, type `pipenv graph`.

9. If a user wants to download your project and set it up, he can check out the code and run `pipenv install`. This would setup all the required dependencies in a new virtual environment.

### Project setup - Server

1. Check out the project and navigate to the 'server' directory.
2. Run `pipenv install` to install dependencies.
3. Run `pipenv run python service.py` to get the server side code running.