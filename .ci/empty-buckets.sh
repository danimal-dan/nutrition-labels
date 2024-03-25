#!/bin/bash

# This script is intended to empty the buckets created by Cloud Formation so that the stack can be rolled back and deleted.

aws s3 rm s3://nutrition-labels-build --recursive --include "*"
aws s3 rm s3://nutrition-labels-lambda --recursive --include "*"
aws s3 rm s3://nutrition-labels-webapp --recursive --include "*"
