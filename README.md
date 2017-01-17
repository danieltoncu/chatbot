# chatbot
[uaic] [fii] [a3] [ai] chatbot

# HowTo Guide (Linux):

## Requirements:

> __Git__

> __Python 2.7, Pip__

> __virtualenv__ ([how to install?](http://docs.python-guide.org/en/latest/dev/virtualenvs/))


### 1. Clone this repository to your local machine:
```bash
git clone https://github.com/danieltoncu/chatbot
```

### 2. Create a virtual environment for Python:
```bash
cd chatbot
virtualenv -p /usr/bin/python2.7 .venv
```
> Note: More information about virtual environments you can find [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

### 3. Once a virtual environment was created, you should activate it:
```bash
source .venv/bin/activate
```

### 4. Install project requirements:
```bash
pip install -r requirements.txt
```

### 5. Now you can start the application:
```bash
python chatbot/main.py [--multiple-answers]
```


### Congratulations! :)
### A CherryPy server was started.
### You can access [Home](http://localhost:8080/) page at the following link: <http://localhost:8080/>.
