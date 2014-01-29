#!/usr/bin/env python

import storage

i = 0
for key in storage.bucket:
	if i == 200:
		break
	i += 1
	print key.name.split('/')[-1]
