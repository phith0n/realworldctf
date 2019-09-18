import flask
import redis
from flask_login import login_required, login_user, current_user, logout_user
from bookhub import app, db, rds
from bookhub.forms import LoginForm, UserForm
from bookhub.models import User, Book
from bookhub.helper import get_remote_addr


user_blueprint = flask.Blueprint('user', __name__, template_folder='templates')


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(data=flask.request.data)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=form.remember_me.data)

        return flask.redirect(flask.url_for('book.admin'))

    return flask.render_template('login.html', form=form)


@user_blueprint.route('/admin/logout/')
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('user.login'))


if app.debug:
    """
    For CTF administrator, only running in debug mode
    """

    @user_blueprint.route('/admin/system/')
    @login_required
    def system():
        """


        :return:
        """

        ip_address = get_remote_addr()
        user_count = User.query.count()
        book_count = Book.query.count()

        return flask.render_template('system.html',
                                     ip_address=ip_address,
                                     user_count=user_count,
                                     book_count=book_count
                                     )

    @user_blueprint.route('/admin/system/change_name/', methods=['POST'])
    @login_required
    def change_name():
        """
        change username

        :return: json
        """

        user = User.query.get(current_user.id)
        form = UserForm(obj=user)
        if form.validate_on_submit():
            form.populate_obj(user)

            db.session.commit()
            return flask.jsonify(dict(status='success'))
        else:
            return flask.jsonify(dict(status='fail', errors=form.errors))


    @login_required
    @user_blueprint.route('/admin/system/refresh_session/', methods=['POST'])
    def refresh_session():
        """
        delete all session except the logined user

        :return: json
        """

        status = 'success'
        sessionid = flask.session.sid
        prefix = app.config['SESSION_KEY_PREFIX']

        if flask.request.form.get('submit', None) == '1':
            try:
                rds.eval(rf'''
                local function has_value (tab, val)
                    for index, value in ipairs(tab) do
                        if value == val then
                            return true
                        end
                    end
                
                    return false
                end
                
                local inputs = {{ "{prefix}{sessionid}" }}
                local sessions = redis.call("keys", "{prefix}*")
                
                for index, sid in ipairs(sessions) do
                    if not has_value(inputs, sid) then
                        redis.call("del", sid)
                    end
                end
                ''', 0)
            except redis.exceptions.ResponseError as e:
                app.logger.exception(e)
                status = 'fail'

        return flask.jsonify(dict(status=status))
