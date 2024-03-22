#!/bin/bash

# CODEPIPELINE_STACK_NAME="nutrition-labels"
# temp to generate a unique name
CODEPIPELINE_STACK_NAME="nutrition-labels-$(date +%Y-%m-%d-%H-%M-%S)"

githubAuthToken=""

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        --github-auth-token=*)
        githubAuthToken="${arg#*=}"
        shift # Remove processed argument
        ;;
        *)    # Unknown option
        ;;
    esac
done

if [ -z ${githubAuthToken} ]
then
	echo "PIPELINE CREATION FAILED!"
        echo "--github-auth-token argument is required"
	exit 1
fi

aws cloudformation create-stack \
        --capabilities CAPABILITY_IAM \
        --stack-name $CODEPIPELINE_STACK_NAME \
        --parameters ParameterKey=GitHubOAuthToken,ParameterValue=${githubAuthToken} \
        --template-body file://$(dirname "$0")/001-cloud-formation-infra-and-codebuild.yaml \
        --region us-east-1 \
        --profile default
