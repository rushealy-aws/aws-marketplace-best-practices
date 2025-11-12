# AWS Marketplace AMI Intellectual Property Protection

Best practices and code examples for protecting intellectual property when publishing AMIs to AWS Marketplace.

## Quick Start

```bash
# Verify your AMI is running on legitimate AWS Marketplace instance
./scripts/verify-marketplace-instance.sh

# Example license validation
python3 examples/license_validator.py
```

## Protection Strategies

### 1. Secrets Protection
- ❌ No hardcoded credentials, private keys, or passwords
- ✅ Use AWS Secrets Manager for license keys
- ✅ Implement IAM roles instead of embedded credentials

### 2. Binary Protection
- ✅ Code obfuscation before AMI packaging
- ✅ Runtime decryption using instance-specific keys
- ✅ Dynamic component loading from secure sources

### 3. Licensed Content Protection
- ✅ Product code verification via EC2 metadata
- ✅ Phone-home licensing validation
- ✅ AWS Marketplace metering integration

## AWS Marketplace Requirements

- AMIs must pass security scanning (no vulnerabilities/malware)
- No encrypted EBS snapshots or filesystems allowed
- Self-service deployment without seller access to instances
- External dependencies must be disclosed

## Files

- `scripts/` - Shell scripts for instance verification
- `examples/` - Python examples for license validation
- `templates/` - CloudFormation templates with IAM roles
- `docs/` - Detailed implementation guides

📖 **[Read the detailed Implementation Guide](docs/implementation-guide.md)** for step-by-step instructions and code examples.

## AWS Documentation References

- [Best practices for building AMIs for AWS Marketplace](https://docs.aws.amazon.com/marketplace/latest/userguide/best-practices-for-building-your-amis.html)
- [AMI-based product requirements for AWS Marketplace](https://docs.aws.amazon.com/marketplace/latest/userguide/product-and-ami-policies.html)
- [AWS Marketplace security](https://docs.aws.amazon.com/marketplace/latest/userguide/security.html)
- [AWS Secrets Manager integration](https://docs.aws.amazon.com/secretsmanager/latest/userguide/integrating_how-services-use-secrets_marketplace-deployment.html)
- [EC2 Instance metadata and user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html)
- [Guidelines for Shared Linux AMIs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/building-shared-amis.html)

## License

MIT License - See LICENSE file for details.
