#!/bin/sh
python ./install.py; gunicorn --chdir app main:api -w 2 --threads 2 -b 0.0.0.0:8000 --log-level debug