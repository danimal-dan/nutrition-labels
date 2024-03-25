# Cloud Formation Deployment

The Cloud Formation is split up into multiple steps.

1. `create-stack.sh` - Creates the required buckets, code pipeline, and API gateway.
2. `functions/*` - Each function has its own Cloud Formation stack to create the function and register an endpoint on the API gateway for calling the function. This Cloud Formation stack is deployed by Code Pipeline.
