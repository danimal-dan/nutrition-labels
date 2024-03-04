# nutrition-labels

Store, arrange, and print nutrition labels for food sent to daycare.

# AWS Sam Cloud Formation Deployment

Command:

```bash
sam sync --template .ci/cloud_formation_template.yaml --s3-bucket nutrition-labels-cloud-formation --stack-name NutritionLabels --region us-east-1 --no-dependency-layer --no-watch --parameters ParameterKey=GitHubOAuthToken,ParameterValue=
```
