# Expense Management System

An web-based expense management system, using Django, that allows automation in the documentation by using Computer Vision and Opticial Character Recognition.

Different formats of installation and setup instructions can be found in the 'Instructions' folder.

The default user for testing is:

-  Username : test
-  Password : password



# Installation and setup instructions

## Prerequisites

### Python 3.8

Python 3 or higher is required to run this project. In order to avoid any compatibility issues it is reccommended getting the most up to date version.

#### Check if already installed

First, to check if Python is already installed open up command prompt or terminal and type:
```
python -V
```

This will print something like ``` Python 3.8.2 ``` if python is installed.
If this shows a version below ``` 3.0.0 ``` then please type the following 
command to check if both are installed at the same time:
```
python3 -V 
```
If this shows a version of 3.0 or higher, then the correct version of python is
installed, skip to 'Checking if pip is installed'. Otherwise, follow the next
steps.

#### Install Python

To install python on Windows or MacOS, download the most up to date version 
[here](https://www.python.org/downloads/). The current version is 3.8.2.

During the installation there will be an option to 
'add Python \<version\> to PATH'. Please ensure this is checked.
Once complete please attempt to get check it is installed using the previous 
chapter

##### Windows 10

Alternatively if on windows 10 you can navigate to the windows store and search 
for python 3.8. This will automatically install and setup python as needed for 
this project.


### Checking if pip is installed

By installing python 3.8 or above Pip should be automatically installed along 
side it. To check it is installed go to command prompt or terminal type:
```
   pip -V
```
With some installations this command does not work without referencing python 
first. If this did not work, please try one of the below commands. Usually the 
```python``` or ```python3``` command that worked when checking the version 
earlier will be the correct one. If both provided the same value, either should
work.
```
python -m pip -V

python3 -m pip -V
```
Please remember the working comand as it will be needed throughout the 
rest of the installation.
Now Python and Pip are running we need to set up the virtual environment and
install dependencies.


## Setting up the Virtual Environment

Open command prompt or terminal and set the directory to the root of the project
files. If the project files are on your desktop it would look like this:
```
cd Desktop/ems-python
```

Once in this location, by using the command that worked for python version 
``` 3.0.0 ``` or above type one of these:

```
python -m venv venv

python3 -m venv venv
```

Now the dependencies for the project need installed. By using the command that
made pip work earlier, type one of the following:

```
pip install -r requirements.txt

python -m pip install -r requirements.txt

python3 -m pip install -r requirements.txt

```
Now the environment needs activated. Please follow the steps for your operating
system

### Windows

In command prompt, navigate to the folder 'venv/Scripts' within the root
directory. If already in the root directory, type this:
``` 
cd venv/Scripts
```
Now type the following command:
```
activate 
```
To confirm it is working you should see ```(venv)``` before the current
directory within command prompt.


### MacOS 

In terminal within the root directory of the project type the following command
```
source venv/bin/activate
```
To confirm it is working you should see ```(venv)``` before the current
directory within the terminal.

## Running the server

To run the server ** open a new command prompt or terminal window ** making sure
to leave the virtual environment running in the one that has just been set up.

Navigate to the root directory of the project following the same command as
earlier. If this is in desktop then it would look like:

```
cd Desktop/ems-python
```

Finally type the following command to run the server using the python command
used earlier:

``` 
python manage.py runserver

python3 manage.py runserver
```

Once this is complete the server should be running and accessible at this link
[localhost:8000](localhost:8000)


## Clean up

Once done with the server and environment simply follow these steps

### Stop Server

To stop the server running simply press the following buttons on the command
prompt or terminal running the server:

```  
Control + C
```

### Deactivate

To deactivate the environment simple type the following command on the command
prompt or teminal running the environment:

```
deactivate
```



