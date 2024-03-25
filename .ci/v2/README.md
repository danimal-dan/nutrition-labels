Now that we have things working, let's try a V2.

Goal:

- One Cloudformation file to setup the pipelines and API Gateway (sans lambda)

In the first version, I separated out the API Gateway setup into a separate cloud formation file to avoid issues with the code for the lambda function not being available immediately (code is available when codepipeline/build completes)

After getting a little more experience, I think I can redesign this thing.

Process:

- Put bucket creation, codepipeline and API gateway into a single Cloud formation file, but do not add the _path_ for the lambda function yet.
- As part of the Lambda's codepipeline, it will not only deploy the code as it does in v1, but will also deploy a Cloudformation stack for the lambda function
  - This Cloudformation file will create the lambda function resource AND add a path to proxy to the function on the existing API Gateway
