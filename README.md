# PyServer

PyServer is a server built as the main data storage, it can be used by both MyFit and PyBot to store data without any distinction. Moreover, the PyServer has the task of predicting emotions on the images provided by the PyBot.

PyServer is developed in Python.

## Installation

In this section are described all the steps required to install and deploy the PyServer.

### Step 1 - Software requirements

- Install the latest version of Python3
- Install the latest version of Pip3
- From terminal move to the project root folder
- Install python requirements

```bash
sudo pip3 install -r requirements.txt
```

### Step 2 - Configuration

- In the project root folder open the file "settings.py"

```python
FLASK_SERVER_NAME = 'http://192.168.43.115:3000'
FLASK_DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@db_url/db_name'

JWT_SECRET_KEY = 'key123'

SAVE_IMG = True
```

- Change **FLASK\_SERVER\_NAME** with the URL where will be deployed PyServer
- Change **FLASK\_DEBUG** to *False* if you don't want to show the debug messages otherwise leave *True*
- In **SQLALCHEMY\_DATABASE\_URI** change:
  - username: username of your db account
  - password: password of your db account
  - db\_url: URL of your db
  - db\_name: name of your db

- Change **JWT\_SECRET\_KEY** with the password that you prefer
- Change **SAVE\_IMG** to *False* if you don't want to save the images of emotion recognition otherwise leave *True*

### Step 3 - Deployment

- From the terminal move to the root folder of the project
- Run the command:

```bash
sudo python3 main.py
```
