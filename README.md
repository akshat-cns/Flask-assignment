# Event Management application using Flask

### Setup
Create project with virtual environment

```console
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
```

Activate it
```console
$ . venv/bin/activate
```

or on Windows
```console
venv\Scripts\activate
```

Install Dependencies
```console
$ pip install Flask
$ pip install Flask-SQLAlchemy
```

Set environment variables in terminal
```console
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
```

or on Windows
```console
$ set FLASK_APP=app.py
$ set FLASK_ENV=development
```

Run the app
```console
$ flask run
```


## Admin functionality
- View all events
- Add a new event
- Update event details
- Delete event

## User functionality
- View available events
- Book tickets for an event
- Cancel booking
