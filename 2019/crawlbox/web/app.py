import requests
import flask
import redis
import validators
import functools
from flask import Flask, request
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)
app.secret_key = 'E%g5r%J7wE73'
rdb = redis.from_url('redis://:QzFs0WGD3koT@redis:6379/0')
base = 'http://127.0.0.1:6800'


def get_ipaddress(request: flask.Request):
    return request.headers.get("x-forwarded-for", request.remote_addr)


def check_throttle(func):
    @functools.wraps(func)
    def view(*args, **kwargs):
        ip_address = get_ipaddress(flask.request)
        if flask.request.method != 'POST':
            return func(*args, **kwargs)

        if rdb.get(ip_address) is None:
            rdb.set(ip_address, 1, ex=10)
            return func(*args, **kwargs)
        else:
            flask.flash('Your request is too frequent', 'warning')
            return flask.redirect(flask.url_for('index'))

    return view


def get_links(base):
    links = rdb.smembers(base)
    return [link.decode() for link in links]


@app.route('/', methods=['GET', 'POST'])
@check_throttle
def index():
    if request.method != 'POST':
        url = flask.session.get('url', '')
        links = get_links(url) if url else set()
        return flask.render_template('index.html', links=links)

    url = request.form.get("url", "")
    if not validators.url(url, public=True):
        flask.flash('URL is error', 'danger')
        return flask.redirect(flask.url_for('index'))

    flask.session['url'] = url
    try:
        app.logger.info('crawl for %s', url)
        response = requests.post(f'{base}/schedule.json', data={
            'project': 'webpage_1o24',
            'spider': 'page',
            'url': url
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('status', '') == 'ok':
                flask.flash('Waiting for crawling then refreshing the page to get results...', 'success')
                return flask.redirect(flask.url_for('index'))
    except Exception as e:
        app.logger.warning('request %s/schedule.json failed, exception %s', base, str(e))

    flask.flash('Crawling fail...', 'danger')
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
    app.run()
