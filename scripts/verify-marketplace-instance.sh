#!/bin/bash
# Verify instance is running from AWS Marketplace AMI
# 
# References:
# - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
# - https://docs.aws.amazon.com/marketplace/latest/userguide/best-practices-for-building-your-amis.html

set -e

# Get IMDSv2 token
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "ERROR: Cannot obtain IMDS token - not running on EC2"
  exit 1
fi

# Get instance identity document
IDENTITY=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/dynamic/instance-identity/document 2>/dev/null)

# Get product codes
PRODUCT_CODES=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/product-codes 2>/dev/null)

# Verify product code exists (replace with your actual product code)
EXPECTED_PRODUCT_CODE="your-product-code-here"

if echo "$PRODUCT_CODES" | grep -q "$EXPECTED_PRODUCT_CODE"; then
  echo "✅ Valid AWS Marketplace instance"
  echo "Product Code: $EXPECTED_PRODUCT_CODE"
  exit 0
else
  echo "❌ Invalid instance - not launched from AWS Marketplace"
  echo "Found codes: $PRODUCT_CODES"
  exit 1
fi
