# SRpract
There is a couple steps to run the code.

## First clone the repository to your local machine. 
To do this, run the following command in the terminal in the directory you want to clone the repository to: 'git clone https://github.com/JernoBeuker/SRpract'.

## Making a virtual environment
The next step is to make a virtual environment with all the libraries listed in the requirements.txt file.
To make a virtual environment using venv, run the following command: 'python -m venv PATH_TO_VENV python=PYTHON_VERSION(optional)'. PATH_TO_VENV and PYTHON_VERSION are placeholders and should be changed (or left out in case of the python version as it is an optional argument).
To put the requirements in the virtual environment, run the following code: 'pip install -r requirements.txt'

## Filling in the global variables
For the program to run, it is imperative to fill in the global variables in the ass/ass1.py file. The two variables that need to be filled in is the 'REALM' variable, which is the realm that connects the program to the robot. The other global variable that should be filled in is the 'GEMINI_API_KEY', which is a key to access the Gemini API, which is needed for the robot to engage in conversation.

## Runing the code
To run the code, go to the main folder 'SRpract', and type in the command: 'python3 ass/ass1.py'
