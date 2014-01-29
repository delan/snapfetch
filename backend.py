#!/usr/bin/env python

import config
import errors
import storage
import os
import time
import sqlite3

conn = sqlite3.connect(os.path.join('data', 'db.sqlite'))

def usage():
	"""Get the number of Glacier restores started in the last 24 hours."""
	t = int(time.time()) - 86400
	r = conn.execute('SELECT COUNT(*) FROM restores WHERE time > ?', (t, ))
	return r.fetchone()[0]

def restore(hash):
	"""Restore the file with the given hash, noting it in the database."""
	if usage() < config.max_daily:
		key = storage.key(hash)
		storage.restore(key)
		conn.execute('INSERT INTO restores (hash, done, time) \
		              VALUES (?, 0, ?)', (hash, int(time.time())))
		conn.commit()
	else:
		raise errors.ExceededQuotaError

def retrieve(hash):
	"""Get the download URL for a file, or None if still restoring."""
	key = storage.key(hash)
	status = storage.status(key)
	if status == storage.STATUS_FROZEN:
		restore(hash)
	elif status == storage.STATUS_LIVE:
		# TODO: update until field in database for restoration expiry?
		return storage.url(key)
	elif status == storage.STATUS_RESTORING:
		pass
