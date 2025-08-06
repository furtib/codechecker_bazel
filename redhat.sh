#!/bin/bash
docker build --network host -t rhel-test-env ./redhat
docker run -it --rm -v $(pwd):/app --network host rhel-test-env