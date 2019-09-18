import flask
from bookhub import login_manager, migrate
from .user import User
from .book import Book


__all__ = ['User', 'Book']


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect(flask.url_for('user.login'), code=303)
