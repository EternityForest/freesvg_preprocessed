#!/usr/bin/env python3
import os
import sys
import shutil

def path(dr, f): return os.path.join(dr, f)

def processNonAlpha(c):
	try:
		return str(int(c))
	except:
		return 'misc'

dr = sys.argv[1]
for f in os.listdir(dr):
    fsrc = path(dr, f)
    if os.path.isfile(fsrc):
        s = f[0]; target = path(dr, s.upper()) if s.isalpha() else path(dr, processNonAlpha(s))
        if not os.path.exists(target):
            os.mkdir(target)
        shutil.move(fsrc, path(target, f))
