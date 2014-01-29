#!/usr/bin/env python

class SnapfetchError(Exception):
	"""Base class for all exceptions raised by Snapfetch."""
	pass

class NoSuchKeyError(SnapfetchError):
	"""The requested key does not exist in S3."""
	pass

class ExceededQuotaError(SnapfetchError):
	"""The operation failed due to too many recent restorations."""
	pass

class AlreadyRestoredError(SnapfetchError):
	"""The file to be restored has already been restored."""
	pass

class AlreadyRestoringError(SnapfetchError):
	"""The file to be restored is currently undergoing restoration."""
	pass
