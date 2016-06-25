# University Database Project

In order to run this app you need to have [Python 3](https://www.python.org/) installed.

Also, you need:
* [Flask](https://github.com/pallets/flask)
* [Peewee ORM](https://github.com/coleifer/peewee)
* [Faker](https://github.com/joke2k/faker)
* [WTForms](https://github.com/wtforms/wtforms)
* [Flask-WTF](https://github.com/lepture/flask-wtf)

**Run this command inside project directory to install dependencies:**
```
pip install -r requirements.txt
```

**Start server:**
```
python app.py
```

## If you want to create isolated environment for application:

Install and create virtualenv:
```
pip install virtualenv
virtualenv venv
```
Then, if you are on Windows, run this:
```
venv\Scripts\activate.bat
```
Or if you are on Mac or Linux:
```
source venv/bin/activate
```
And then run:
```
pip install -r requirements.txt
```
