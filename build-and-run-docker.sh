#!/bin/bash
docker build --network host -t my-test-env .
docker run -it --rm -v $(pwd):/app --network host my-test-env