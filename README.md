## Setting up Database ##
```
$ fask shell

>>> from src import db
>>> db.create_all()
>>> quit()

$ flask db init
...
$ flask db upgrade
```

## Setting up Mail
```
$ export MAIL_USERNAME=<gmail address>
$ export MAIL_PASSWORD=<password to the gmail>
$ export FLASK_ADMIN=<gmail address>
```