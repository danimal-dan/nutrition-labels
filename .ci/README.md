# Cloud Formation Deployment

The Cloud Formation is split up into multiple steps.

1. `create-stack.sh` - Creates the required buckets, code pipeline, and API gateway.
2. `functions/*` - Each function has its own Cloud Formation stack to create the function and register an endpoint on the API gateway for calling the function. This Cloud Formation stack is deployed by Code Pipeline.

# Deployment

Run `create-stack.sh` and provide the following parameters:

- `--github-auth-token` - Access token to Github repository
- `--hosted-zone-id` - Zone Id in Route 53 for the domain
- `--domain-name` - Custom domain name to be used in API Gateway, corresponds to `--hosted-zone-id`
- `--ssl-certificate-arn` - SSL certificate for domain name
