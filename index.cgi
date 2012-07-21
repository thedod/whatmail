#!/bin/sh
# This wrapper is not necessarily needed, but some places (e.g. webffaction)
# require extra env etc. for gpgme to work, so here you can write something like:
#   LD_LIBRARY_PATH=/path/to/lib /path/to/my/python whatmail.py
# Normally, this should work:
env python whatmail.py
