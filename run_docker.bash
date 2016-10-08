#!/bin/bash
docker run -t --rm --name docker-check-script -v /home/rein/git/zipgradegenerator/test_uploads/$1:/usr/src/myapp.py -v /home/rein/git/zipgradegenerator/checkSubmission.py:/usr/src/checkSubmission.py -w /usr/src/ pythondoc python3 checkSubmission.py myapp.py
