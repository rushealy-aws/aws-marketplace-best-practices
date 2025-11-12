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

## License

MIT License - See LICENSE file for details.
