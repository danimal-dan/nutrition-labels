A Single cloud formation file wasn't working

We'll break it into steps:

1. `001-cloud-formation-infra.yaml` - Sets up the bucket for the Nutrition Labels application, and the CodeBuild and Deploy Pipelines
2. `002-lambda-pdf-generator-deployment.yaml` - Used to deploy the built function to AWS Lambda - this one uses the SAM transformer
3. `002-cloud-front-and-api-gateway.yaml` - Afer the applications are built and stored in S3, sets up Cloudfront and the API Gateway
