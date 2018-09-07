import os
import datetime
from uuid import uuid4
from flask import (Flask, request, make_response, render_template,
                   Response, abort, redirect, url_for)

app = Flask(__name__)


def standard_response(response_object, request_object):
    resp = make_response(response_object)
    resp.headers['X-HELLO'] = 'WORLD!'

    if 'uid' not in request_object.cookies:
        ts = datetime.datetime.today().strftime('%s')
        new_cookie = str(uuid4())
        resp.set_cookie('uid', value=new_cookie)
        with open('db.log', 'a') as f:
            line = '{0}-{1}\n'.format(ts, new_cookie)
            f.write(line)

    else:
        ts = datetime.datetime.today().strftime('%s')
        uid = request_object.cookies['uid']
        with open('db.log', 'a') as f:
            line = '{0}-{1}\n'.format(ts, uid)
            print line
            f.write(line)

    return resp


@app.route('/')
def home():
    resp = standard_response(
        render_template('home.html'),
        request
    )
    return resp


@app.route('/new/', methods=['POST'])
def new():
    pb = request.form['pb'].encode('utf-8')

    if len(pb) < 1:
        return redirect('/', 302)

    ts = datetime.datetime.now().strftime('%s')
    fn = 'static/pastes/{}'.format(ts)
    with open(fn, 'w') as f:
        f.write(pb)

    return_url = 'http://pb.billben.net/get/{}/'.format(ts)
    return Response(
        return_url,
        mimetype='text/plain'
    )


@app.route('/get/<lu>/', methods=['GET'])
def get(lu):
    path = 'static/pastes/{}'.format(lu)

    if not os.path.exists(path):
        abort(418)

    with open(path, 'r') as f:
        return Response(
            f.read(),
            mimetype='text/plain'
        )


@app.route('/help/', methods=['GET'])
def help():
    return Response(
        '',
        # render_template('help.txt'),
        mimetype='text/plain'
    )


@app.route('/list/', methods=['GET'])
def list():
    return_text = '\n'.join(os.listdir('static/pastes'))
    return Response(
        return_text,
        mimetype='text/plain'
    )


@app.route('/del/<id>/', methods=['GET'])
def delete(id):
    if not os.path.exists('static/pastes/{}'.format(id)):
        abort(418)
    else:
        os.remove('static/pastes/{}'.format(id))
        return redirect('/', 302)


if __name__ == '__main__':
    app.run(debug=True, port=8081, host='0.0.0.0')
