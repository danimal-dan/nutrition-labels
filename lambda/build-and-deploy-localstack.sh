#!/bin/bash

rm -rf build/
mkdir build
pip install \
    --platform manylinux2014_x86_64 \
    --target=build/ \
    --implementation cp \
    --python-version 3.11 \
    --only-binary=:all: --upgrade \
    -r requirements.txt
cp *.py ./build

if awslocal lambda get-function --function-name pdf-generator; then
    awslocal lambda update-function-code --function-name pdf-generator --s3-bucket "hot-reload" --s3-key "$(pwd)/build/"
    awslocal lambda get-function-url-config --function-name pdf-generator
else
    awslocal lambda delete-function --function-name pdf-generator
    awslocal lambda create-function --function-name pdf-generator --timeout 60 --code S3Bucket="hot-reload",S3Key="$(pwd)/build/" --handler GeneratePdfHandler.lambda_handler --role arn:aws:iam::000000000000:role/test-role --runtime python3.11
    awslocal lambda create-function-url-config --function-name pdf-generator --auth-type NONE --cors '{"AllowHeaders": ["*"],"AllowOrigins": ["*"],"AllowMethods": ["*"], "AllowCredentials": false}'
fi
