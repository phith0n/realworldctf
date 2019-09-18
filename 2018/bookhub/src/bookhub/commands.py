import os
import click
import datetime
import getpass
from urllib.parse import urlparse

from bookhub import app, db
from bookhub.models import User, Book


@app.cli.command()
def init():
    pass


@app.cli.command()
def createuser():
    username = input('Input username: ')
    password = getpass.getpass('Input password: ')
    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()


@app.cli.command()
def createbook():
    title = input('Input book title: ')
    description = input('Input book description: ')
    img = input('Input a img url: ')

    book = Book(
        title=title,
        description=description,
        img=img,
        created_at=datetime.datetime.now()
    )
    db.session.add(book)
    db.session.commit()
