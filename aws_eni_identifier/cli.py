import json
import sys

import typer
from glom import glom
from rich.console import Console
from rich.table import Table

import aws_eni_identifier as aei


def partialy_sorted(_list: list, order: list) -> list:
    unordered = [e for e in _list if e not in order]
    mapping = order + unordered
    return sorted(_list, key=mapping.index)


def create_table(_list: list[dict], columns_order: list[str]):
    headers = partialy_sorted(
        list({key for _dict in _list for key in _dict.keys()}), order=columns_order
    )

    table = Table(*headers, show_lines=True)
    for _dict in _list:
        table.add_row(*[_dict.get(key) for key in headers])
    return table


app = typer.Typer()

DEFAULT_EXTRA_FIELDS = ["sg-names"]


@app.command()
def main(
    add_column: list[str] = typer.Option(
        default=DEFAULT_EXTRA_FIELDS,
        help="Add extra columns: --add-column Attachment.Status --add-column AvailabilityZone",
    ),
    input: typer.FileText = typer.Option(
        default="-", help="File path. STDIN by default", show_default=False
    ),
    output: typer.FileTextWrite = typer.Option(
        default="-", help="File path. STDOUT by default", show_default=False
    ),
    _json: bool = False,
):
    """Identify AWS network interfaces owner service.

    aws ec2 describe-network-interfaces --profile my-profile | aws-eni-identifier
    """
    try:
        _loaded = json.load(input)
        if isinstance(_loaded, dict):
            enis = _loaded.get("NetworkInterfaces", [])
        else:
            enis = _loaded
    except json.decoder.JSONDecodeError as e:
        typer.echo(f"JSONDecodeError: {e}", err=True)
        sys.exit(1)

    result = []
    for eni in enis:
        info = aei.identify_eni(eni)
        result.append(info | add_columns(eni, columns=add_column))

    if _json:
        output.write(json.dumps(result))
    else:
        console = Console()
        table = create_table(result, columns_order=["eni", "svc", "name"])
        console.print(table, new_line_start=True)


def add_columns(eni: dict, columns: list[str]):
    result = {}

    for column in columns:
        if column == "sg-names":
            extra = glom(eni, ("Groups", ["GroupName"]))
        elif column == "sg-ids":
            extra = glom(eni, ("Groups", ["GroupId"]))
        else:
            extra = glom(eni, column, default=None)
        if isinstance(extra, list):
            extra = ", ".join(extra)
        result[column] = extra
    return result
