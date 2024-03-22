#!/bin/bash

# CODEPIPELINE_STACK_NAME="nutrition-labels"
# temp to generate a unique name
CODEPIPELINE_STACK_NAME="nutrition-labels-lambda-and-gateway-$(date +%Y-%m-%d-%H-%M-%S)"

domainName=""
hostedZoneId=""
webAppBucketEndpoint=""
webAppBucketName=""
sslCertificateArn=""

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        --domain-name=*)
        domainName="${arg#*=}"
        shift # Remove processed argument
        ;;
        --hosted-zone-id=*)
        hostedZoneId="${arg#*=}"
        shift # Remove processed argument
        ;;
        --web-app-bucket-endpoint=*)
        webAppBucketEndpoint="${arg#*=}"
        shift # Remove processed argument
        ;;
        --web-app-bucket-name=*)
        webAppBucketName="${arg#*=}"
        shift # Remove processed argument
        ;;
        --ssl-certificate-arn=*)
        sslCertificateArn="${arg#*=}"
        shift # Remove processed argument
        ;;
        *)    # Unknown option
        ;;
    esac
done

if [ -z ${domainName} ]
then
	echo "PIPELINE CREATION FAILED!"
        echo "--domain-name argument is required"
	exit 1
fi

if [ -z ${hostedZoneId} ]
then
	echo "PIPELINE CREATION FAILED!"
        echo "--hosted-zone-id argument is required - Route53 Hosted Zone Id"
	exit 1
fi

if [ -z ${webAppBucketEndpoint} ]
then
	echo "PIPELINE CREATION FAILED!"
        echo "--web-app-bucket-endpoint argument is required"
	exit 1
fi

if [ -z ${webAppBucketName} ]
then
	echo "PIPELINE CREATION FAILED!"
        echo "--web-app-bucket-name argument is required"
	exit 1
fi

if [ -z ${sslCertificateArn} ]
then
	echo "PIPELINE CREATION FAILED!"
        echo "--ssl-certificate-arn argument is required"
	exit 1
fi

aws cloudformation create-stack \
        --capabilities CAPABILITY_IAM \
        --stack-name $CODEPIPELINE_STACK_NAME \
        --parameters ParameterKey=CustomDomainName,ParameterValue=${domainName} \
        ParameterKey=HostedZoneId,ParameterValue=${hostedZoneId} \
        ParameterKey=WebAppBucketEndpoint,ParameterValue=${webAppBucketEndpoint} \
        ParameterKey=WebAppBucketName,ParameterValue=${webAppBucketName} \
        ParameterKey=SslCertificateArn,ParameterValue=${sslCertificateArn} \
        --template-body file://$(dirname "$0")/002-cloud-formation-deploy-lambda-and-api-gateway.yaml \
        --region us-east-1 \
        --profile default
