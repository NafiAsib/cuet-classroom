# CUET Classroom

Requirements:
___
* Pyhton 3
* Flask, SQLAlchemy, Bcrypt, WTForms
```
  pip install flask
  pip install flask-sqlalchemy
  pip install flask-bcrypt
  pip install flask-login
  pip install flask-wtf
```
* Create a database file
```python
  from classroom import db
  from classroom.models import User, Ct
  db.create_all()
```
* Run the following command and goto localhost:5000
```
  python run.py
```
