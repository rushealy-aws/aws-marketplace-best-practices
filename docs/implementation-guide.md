# Implementation Guide

## AWS Documentation References

### Core Requirements
- [AMI-based product requirements](https://docs.aws.amazon.com/marketplace/latest/userguide/product-and-ami-policies.html){:target="_blank"} - Official AWS Marketplace policies
- [Best practices for building AMIs](https://docs.aws.amazon.com/marketplace/latest/userguide/best-practices-for-building-your-amis.html){:target="_blank"} - Security and build guidance

### Security & Secrets
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html){:target="_blank"} - Managing secrets securely
- [Store and use secrets securely](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/sec_identities_secrets.html){:target="_blank"} - Well-Architected Framework
- [Guidelines for Shared Linux AMIs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/building-shared-amis.html){:target="_blank"} - EC2 AMI security

### Instance Verification
- [Instance metadata and user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html){:target="_blank"} - EC2 metadata service
- [Instance identity documents](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html){:target="_blank"} - Verification methods

## Secrets Protection

### What NOT to Include in AMI
```bash
# ❌ NEVER include these in your AMI
/etc/ssh/ssh_host_*_key      # SSH host keys
~/.ssh/id_rsa                # Private keys
/app/config/database.conf    # Hardcoded passwords
/app/licenses/license.key    # License files
```

### Secure Alternatives
```bash
# ✅ Generate SSH keys at boot
ssh-keygen -A

# ✅ Retrieve secrets at runtime
aws secretsmanager get-secret-value --secret-id license-key

# ✅ Use IAM roles for AWS access
aws sts get-caller-identity  # No credentials needed
```

## Binary Protection

### Code Obfuscation Example
```python
# Before AMI packaging, obfuscate critical code
import base64

def obfuscated_function():
    # Original: return "secret_algorithm"
    return base64.b64decode(b'c2VjcmV0X2FsZ29yaXRobQ==').decode()
```

### Runtime Decryption
```python
import hashlib
from cryptography.fernet import Fernet

def decrypt_binary(instance_id):
    # Use instance-specific key
    key = hashlib.sha256(instance_id.encode()).digest()[:32]
    f = Fernet(base64.urlsafe_b64encode(key))
    
    with open('/app/encrypted_binary', 'rb') as file:
        encrypted_data = file.read()
    
    return f.decrypt(encrypted_data)
```

## License Validation Flow

1. **Instance Verification**
   - Get EC2 instance metadata
   - Verify product code matches your AMI
   - Validate instance identity document signature

2. **License Retrieval**
   - Fetch license from Secrets Manager
   - Or validate against external licensing server
   - Cache license locally with expiration

3. **Ongoing Validation**
   - Periodic license checks
   - Handle license renewal
   - Graceful degradation on validation failure

## AWS Marketplace Compliance Checklist

- [ ] No hardcoded secrets in AMI
- [ ] No encrypted EBS snapshots
- [ ] Self-service deployment
- [ ] Security scanning passes
- [ ] External dependencies disclosed
- [ ] IAM roles instead of credentials
- [ ] Product code verification implemented
