# Using the IAM Role Template

This guide shows how to deploy and use the CloudFormation IAM role template for your AWS Marketplace AMI.

## 1. Deploy the CloudFormation Stack

```bash
# Deploy with default secret name
aws cloudformation create-stack \
  --stack-name marketplace-iam-role \
  --template-body file://templates/marketplace-iam-role.yaml \
  --capabilities CAPABILITY_IAM

# Or deploy with custom secret name
aws cloudformation create-stack \
  --stack-name marketplace-iam-role \
  --template-body file://templates/marketplace-iam-role.yaml \
  --parameters ParameterKey=SecretName,ParameterValue=my-license-secret \
  --capabilities CAPABILITY_IAM
```

## 2. Get the Instance Profile ARN

```bash
# Get the instance profile ARN from stack outputs
aws cloudformation describe-stacks \
  --stack-name marketplace-iam-role \
  --query 'Stacks[0].Outputs[?OutputKey==`InstanceProfileArn`].OutputValue' \
  --output text
```

## 3. Use in Your AMI

**Option A: Attach during EC2 launch**
```bash
# Launch instance with the IAM role
aws ec2 run-instances \
  --image-id ami-12345678 \
  --instance-type t3.micro \
  --iam-instance-profile Name=marketplace-iam-role-MarketplaceInstanceProfile-XXXXX
```

**Option B: Include in your AMI's user data script**
```bash
#!/bin/bash
# This role is automatically attached to the instance
# Your application can now access Secrets Manager
python3 /app/license_validator.py
```

## 4. Update Your Python Code

The license validator will automatically use the attached IAM role:

```python
# No AWS credentials needed - uses IAM role
client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='marketplace-license-key')
```

## 5. CloudFormation Template for Your AMI Product

You can also include this role in your AMI product's CloudFormation template:

```yaml
# Include the role template content in your main template
# Then reference it in your EC2 instance:
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-12345678
      InstanceType: t3.micro
      IamInstanceProfile: !Ref MarketplaceInstanceProfile
```

## Permissions Provided

This IAM role provides minimal permissions for:
- Reading secrets from AWS Secrets Manager
- Writing logs to CloudWatch (for debugging/monitoring)
- Following AWS Marketplace security best practices
