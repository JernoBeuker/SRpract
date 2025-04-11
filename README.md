# SRpract
There are a couple steps to run the code.

## First clone the repository to your local machine. 
To do this, run the following command in the terminal in the directory you want to clone the repository to: 'git clone https://github.com/JernoBeuker/SRpract'.

## Making a virtual environment
The next step is to make a virtual environment with all the libraries listed in the requirements.txt file.
To make a virtual environment using venv, run the following command: 'python -m venv PATH_TO_VENV python=PYTHON_VERSION(optional)'. PATH_TO_VENV and PYTHON_VERSION are placeholders and should be changed (or left out in case of the python version as it is an optional argument).
To put the requirements in the virtual environment, run the following code: 'pip install -r requirements.txt'

## Switching to the Final_Project branch
Switch to the branch final_project (type in: 'git checkout final_project')

## Filling in the global variables
For the program to run, it is imperative to make a .env file with the following global variables: 'KEY' and 'REALM'. The realm variable makes the realm that connects the program to the robot. The key is an access key to the Gemini API, which is needed for the robot to engage in conversation.

## Runing the code
To run the code for the final project, go to the final project folder (cd Final_Project), and type in the command: 'python3 main.py'

## Code structure
- In main.py you can find the main functionalities of our program, such as the core game-loop, the setup and interaction with both the robot and Gemini, and functions to calculate and save the user information.
- In utils.py we put some helper functions we call from the main file, and are put in a separate file as to not clutter the main file.
- In config.py you can find all the global data, such as the prompts, gestures, and other global variables.
- In the words directory the wordlists for the five CEFR levels are stored. Keep them there, as the specific paths to these files are used to acces them.
- In Users.json the information of all users is kept.