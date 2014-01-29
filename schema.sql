CREATE TABLE restores (
	hash TEXT,         -- hexadecimal string: 160-bit hash
	done INTEGER,      -- {0, 1} boolean: whether restoration is complete
	time INTEGER,      -- Unix timestamp: when the restore was initiated
	until INTEGER      -- Unix timestamp: when the restored file expires
);
