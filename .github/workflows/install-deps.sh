#!/bin/bash

sudo apt-get update --quiet

sudo apt-get install --no-install-recommends \
  clang \
  clang-tools \
  clang-tidy
