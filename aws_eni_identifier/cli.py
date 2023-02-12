import itertools
import json
import sys
from typing import IO, Literal, Union

import click
import tabulate
from glom import glom

from aws_eni_identifier import identify


@click.command()
@click.argument("ExtraFields", nargs=-1)
@click.option("-i", "--input", type=click.File(), default=sys.stdin, help="Input file name")
@click.option("-o", "--output", type=click.File("w"), default=sys.stdout, help="Output file name")
@click.option("-ot", "--output-type", type=click.Choice(["table", "json"]), default="table", help="How to return output")
def main(extrafields: list[str], input: IO, output: IO, output_type: Union[Literal["table"], Literal["json"]]):
    """Identify AWS network interfaces owner service. stdin

    aws sso login --profile qameta-prod
     aws ec2 describe-network-interfaces --profile qameta-prod | aws-eni-identifier
    aws-vault exec qameta-prod


    # Extra fields
    AvailabilityZone
    Attachment.InstanceOwnerId
    InterfaceType

    Groups.GroupName
    """
    with input:
        try:
            enis = json.load(input)
        except json.decoder.JSONDecodeError as e:
            click.echo("Invalid JSON")
            sys.exit(1)

    if isinstance(enis, dict) and (enis.get("NetworkInterfaces") is not None):
        enis = enis["NetworkInterfaces"]

    result = []
    for eni in enis:
        info = identify.identify_eni(eni)
        extra = get_extra_info(eni, set(extrafields))
        result.append(info | extra)

    if output_type == "table":
        result = tabulate.tabulate(normalize_keys(result), headers="keys", tablefmt="simple_grid", maxcolwidths=50, missingval="?")
    elif output_type == "json":
        result = json.dumps(result)

    output.write(result)


DEFAULT_EXTRA_FIELDS = {"sg-names"}


def get_extra_info(eni, extra_fields: set[str]):
    result = {}

    extra_fields = extra_fields | DEFAULT_EXTRA_FIELDS
    for field in extra_fields:
        if field == "sg-names":
            extra = glom(eni, ("Groups", ["GroupName"]))
        elif field == "sg-ids":
            extra = glom(eni, ("Groups", ["GroupId"]))
        else:
            extra = glom(eni, field, default=None)
        if isinstance(extra, list):
            extra = " ".join(extra)
        result[field] = extra
    return result


def normalize_keys(_list: list[dict]):
    all_keys = set()
    for _dict in _list:
        all_keys.update(_dict.keys())

    for _dict, key in itertools.product(_list, all_keys):
        if key not in _dict.keys():
            _dict[key] = "?"
    return _list
