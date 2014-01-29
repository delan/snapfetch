#!/usr/bin/env python

STATUS_FROZEN    = 0
STATUS_LIVE      = 1
STATUS_RESTORING = 2

import config
import errors
import boto

conn = boto.connect_s3()
bucket = conn.get_bucket(config.bucket_name)

def key(hash):
	"""Get the S3 key object associated with a given hash."""
	a = hash[0:2]
	b = hash[2:4]
	r = '%s/%s/%s' % (a, b, hash)
	key = bucket.get_key(r)
	if key is None:
		raise errors.NoSuchKeyError
	return key

def refresh(key):
	"""Return an updated S3 key object, given a stale key object."""
	return bucket.get_key(key.name)

def status(key):
	"""Determine whether an S3 key is archived, restoring or live."""
	key = refresh(key)
	# Avoid using key.storage_class; it appears to always return 'STANDARD'
	# regardless of the actual state of the object. For more information:
	# https://github.com/boto/boto/issues/1173
	if key.ongoing_restore == True:
		return STATUS_RESTORING
	elif key.ongoing_restore == False:
		return STATUS_LIVE
	elif key.ongoing_restore == None:
		return STATUS_FROZEN

def restore(key):
	"""Attempt to restore a file from Glacier."""
	s = status(key)
	if s == STATUS_FROZEN:
		key.restore(days=config.restore_days)
	elif s == STATUS_LIVE:
		raise errors.AlreadyRestoredError
	elif s == STATUS_RESTORING:
		raise errors.AlreadyRestoringError

def url(key):
	"""Return an ephemeral URL for the given S3 key object."""
	return key.generate_url(config.url_seconds)
