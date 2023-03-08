[![FivexL](https://releases.fivexl.io/fivexlbannergit.jpg)](https://fivexl.io/)
# AWS ENI Identifier
Identify to which AWS service network interface is associated

![aws-eni-identifier-cli.png](https://github.com/fivexl/aws-eni-identifier/raw/master/docs/usage.gif?raw=true)

# Installation

```bash
pip install aws-eni-identifier
```

# Usage
aws-eni-identifier does not connect to AWS by itself, so you will need to load data with aws-cli

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

## Show extra columns
```bash
aws ec2 describe-network-interfaces | 
aws-eni-identifier \
    --add-column Attachment.Status \
    --add-column AvailabilityZone
```
![extra-columns.png](https://github.com/fivexl/aws-eni-identifier/raw/master/docs/extra-columns.png?raw=true)

## Filter
Find unused network interfaces:
```bash 
aws ec2 describe-network-interfaces \
    --filters "Name=status,Values=available" |
aws-eni-identifier
```
Find AWS resource by IP address (you can use public or private IP address)
```bash 
export IP='51.21.223.193';
aws ec2 describe-network-interfaces \
    --query "NetworkInterfaces[?PrivateIpAddresses[?PrivateIpAddress=='${IP}' || Association.PublicIp=='${IP}']]" | 
aws-eni-identifier
```
Determine what is using specific AWS network interface
```bash
aws ec2 describe-network-interfaces \
    --network-interface-ids eni-0068ac3f8786de59a | 
aws-eni-identifier
```

You can find more information about filters and queries in [AWS documentation](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-network-interfaces.html#options)
 

# Developing

Install the package:
```bash
poetry install
```
Run tests:
```bash
poetry run pytest
```