#!/usr/bin/env python3
"""
AWS Marketplace License Validator
Demonstrates secure license validation using EC2 metadata and Secrets Manager
"""

import json
import boto3
import requests
from botocore.exceptions import ClientError

class MarketplaceLicenseValidator:
    def __init__(self, expected_product_code, secret_name=None):
        self.expected_product_code = expected_product_code
        self.secret_name = secret_name
        self.session = requests.Session()
        
    def get_imds_token(self):
        """Get IMDSv2 token"""
        try:
            response = self.session.put(
                'http://169.254.169.254/latest/api/token',
                headers={'X-aws-ec2-metadata-token-ttl-seconds': '21600'},
                timeout=2
            )
            return response.text
        except:
            raise Exception("Cannot obtain IMDS token - not running on EC2")
    
    def verify_marketplace_instance(self):
        """Verify instance launched from AWS Marketplace"""
        token = self.get_imds_token()
        headers = {'X-aws-ec2-metadata-token': token}
        
        # Get product codes
        response = self.session.get(
            'http://169.254.169.254/latest/meta-data/product-codes',
            headers=headers, timeout=2
        )
        
        product_codes = response.text.strip().split('\n')
        
        if self.expected_product_code in product_codes:
            return True
        else:
            raise Exception(f"Invalid instance - expected {self.expected_product_code}")
    
    def get_license_key(self):
        """Retrieve license key from Secrets Manager"""
        if not self.secret_name:
            return None
            
        try:
            client = boto3.client('secretsmanager')
            response = client.get_secret_value(SecretId=self.secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            raise Exception(f"Cannot retrieve license: {e}")
    
    def validate_license(self):
        """Complete license validation"""
        print("🔍 Validating AWS Marketplace license...")
        
        # Step 1: Verify marketplace instance
        self.verify_marketplace_instance()
        print("✅ Valid AWS Marketplace instance")
        
        # Step 2: Get license key if configured
        if self.secret_name:
            license_data = self.get_license_key()
            print(f"✅ License key retrieved from {self.secret_name}")
            return license_data
        
        print("✅ License validation complete")
        return True

if __name__ == "__main__":
    # Example usage
    validator = MarketplaceLicenseValidator(
        expected_product_code="your-product-code-here",
        secret_name="your-license-secret"  # Optional
    )
    
    try:
        validator.validate_license()
        print("🎉 License validation successful!")
    except Exception as e:
        print(f"❌ License validation failed: {e}")
        exit(1)
