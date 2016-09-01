#!/bin/bash
docker run -t --rm --name my-running-script -v /home/rein/git/zipgradegenerator/test_uploads/$1:/usr/src/myapp.py -v /home/rein/git/zipgradegenerator/checkSubmission.py:/usr/src/checkSubmission.py -w /usr/src/ python:3 python checkSubmission.py myapp.py
