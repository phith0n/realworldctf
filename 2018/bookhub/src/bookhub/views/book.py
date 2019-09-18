import flask
from flask_login import login_required, login_user, current_user
from bookhub import app, db
from bookhub.forms import BookForm
from bookhub.models import User, Book


book_blueprint = flask.Blueprint('book', __name__, template_folder='templates')


@book_blueprint.route('/')
def index():
    try:
        page = int(flask.request.args.get('page', 1))
    except ValueError:
        page = 1

    object_list = Book.query.order_by(Book.created_at.desc()).paginate(page, per_page=10, error_out=False)
    object_list.module_name = 'book.index'
    return flask.render_template('index.html', object_list=object_list, is_debug=app.debug)


@book_blueprint.route('/admin/')
@login_required
def admin():
    try:
        page = int(flask.request.args.get('page', 1))
    except ValueError:
        page = 1

    object_list = Book.query.order_by(Book.created_at.desc()).paginate(page, per_page=10, error_out=False)
    object_list.module_name = 'book.admin'
    return flask.render_template('admin.html', object_list=object_list)


@book_blueprint.route('/admin/add/', methods=['GET', 'POST'])
@login_required
def add():
    form = BookForm(data=flask.request.data)
    if form.validate_on_submit():
        book = Book()
        form.populate_obj(book)
        db.session.add(book)
        db.session.commit()
        return flask.redirect(flask.url_for('book.admin'))

    return flask.render_template('add.html', form=form)


@book_blueprint.route('/admin/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit(id):
    book = Book.query.filter_by(id=id).first_or_404()
    form = BookForm(data=flask.request.data, obj=book)
    if form.is_submitted() and flask.request.form.get('delete', None) is not None:
        db.session.delete(book)
        db.session.commit()
        return flask.redirect(flask.url_for('book.admin'))
    elif form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        return flask.redirect(flask.url_for('book.admin'))

    return flask.render_template('edit.html', form=form)
