import re
from typing import Optional

REGEXES = {
    "apigw": re.compile(r"ENI managed by APIGateway"),
    "codestar": re.compile(r"AWS CodeStar Connections"),
    "dax": re.compile(r"DAX"),
    "dir": re.compile(r"AWS created network interface for directory (?P<name>d-[a-z0-9_]+)."),
    "dms": re.compile(r"DMSNetworkInterface"),
    "ecs": re.compile(r"arn:aws:ecs:[a-z0-9-]+:[0-9]+:attachment/(?P<name>[a-zA-Z0-9_]+)"),
    "fsmt": re.compile(r"EFS mount target for (?P<fs>fs-[a-zA-Z0-9-]+) \((?P<name>[a-zA-Z0-9-]+)\)"),
    "elasticache": re.compile(r"ElastiCache (?P<name>.*)"),
    "emr": re.compile(r"AWS ElasticMapReduce"),
    "hsm": re.compile(r"CloudHSM Managed Interface"),
    "hsmv2": re.compile(r"CloudHsm ENI"),
    "lambda": re.compile(r"AWS Lambda VPC ENI-(?P<name>[a-z0-9_]+)-.*"),
    "nat": re.compile(r"Interface for NAT Gateway (?P<name>.*)"),
    "rds": re.compile(r"RDSNetworkInterface"),
    "redshift": re.compile(r"RedshiftNetworkInterface"),
    "tgw": re.compile(r"Network Interface for Transit Gateway Attachment (?P<name>tgw-[a-zA-Z0-9_-]+)"),
    "vpce": re.compile(r"VPC Endpoint Interface (?P<name>.*)"),
    "eks": re.compile(r"Amazon EKS (?P<name>.*)"),
    "es": re.compile(r"ES (?P<name>.*)"),
    "rds-proxy": re.compile(r"Network interface for DBProxy (?P<name>.*)"),
    "kinesis-firehose": re.compile(r"Amazon Kinesis Firehose - (?P<name>.*)."),
    # order is important
    "elb-app": re.compile(r"ELB app/(?P<name>[a-z0-9-]+)/?([a-z0-9]+)?"),
    "elb-net": re.compile(r"ELB net/(?P<name>[a-z0-9-]+)/?([a-z0-9]+)?"),
    "elb-gwy": re.compile(r"ELB gwy/(?P<name>[a-z0-9-]+)/?([a-z0-9]+)?"),
    "elb": re.compile(r"ELB (?P<name>[a-z0-9-]+)/?([a-z0-9]+)?"),
}


def extract_info(description: str) -> Optional[dict]:
    for svc, regex in REGEXES.items():
        if (match := re.search(regex, description)) is not None:
            info = match.groupdict()
            info["svc"] = svc
            return info
