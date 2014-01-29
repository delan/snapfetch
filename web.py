#!/usr/bin/env python

import os
import flask

basedir = os.path.dirname(__file__)
app = flask.Flask(__name__, static_folder=os.path.join(basedir, 'static'))

@app.route('/')
def hello():
	return flask.Response('Hello, world!', mimetype='text/plain')
