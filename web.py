#!/usr/bin/env python

import backend
import errors
import os
import flask

basedir = os.path.dirname(__file__)
app = flask.Flask(__name__, static_folder=os.path.join(basedir, 'static'))

def text(status, content):
	return flask.Response(
	               response=content,
	               status=status,
	               mimetype='text/plain'
	       )

@app.route('/')
def hello():
	return text(200, 'Hello, world!')

@app.route('/blob/<hash>')
def blob(hash):
	try:
		url = backend.retrieve(hash)
		if url is None:
			return text(202, 'File restoration now in progress')
		else:
			# TODO: set Expires header to now + config.url_seconds
			return flask.redirect(location=url, code=307)
	except errors.NoSuchKeyError:
		return text(404, 'No file exists with the given hash')
	except errors.ExceededQuotaError:
		return text(503, 'Too many restorations in the last 24 hours')
