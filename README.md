# aws-eni-identifier
Identify to which AWS service network interface is associated

# Installation
```bash
pip install aws-eni-identifier
```

# Usage
aws-eni-identifier does not connect to AWS by itself, so you will need to load data wit aws-cli

Login to aws:
```bash
aws sso login --profile my-profile
```

Use pipe:
```bash
aws ec2 describe-network-interfaces | aws-eni-identifier
```

Or save to file with aws-cli and read it:
```bash
aws ec2 describe-network-interfaces > ni.json
aws-eni-identifier -i ni.json
```



# Developing

Install the package:
```bash
poetry install
```
Run tests:
```bash
pytest
```