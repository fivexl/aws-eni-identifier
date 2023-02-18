import json
import random
import string

import faker
from glom import assign, glom

import aws_eni_identifier

faker = faker.Faker()


def random_id(prefix: str, length: int):
    def generator():
        id = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        return f"{prefix}{id}"

    return generator


def assign_if_not_none(target, source, spec, missing=dict, transform=None):
    if value := glom(source, spec, default=None):
        if transform:
            value = transform(value)
        if value:
            assign(target, spec, value, missing=missing)


import re

ec2_id_re = re.compile(r".*(?P<ec2_id>i-[a-z0-9]+).*")


def re_groupdict(pattern: re.Pattern, string: str):
    if (match := re.search(pattern, string)) is not None:
        return match.groupdict()


def anonimize(enis: list[dict]):
    results = []
    for eni in enis:
        result = {}

        assign_if_not_none(target=result, source=eni, spec="InterfaceType")
        assign_if_not_none(target=result, source=eni, spec="Attachment.Status")
        assign_if_not_none(target=result, source=eni, spec="AvailabilityZone")

        assign_if_not_none(
            target=result,
            source=eni,
            spec="Description",
            transform=lambda s: None if re_groupdict(ec2_id_re, s) else s,
        )
        assign_if_not_none(
            target=result,
            source=eni,
            spec="RequesterId",
            transform=lambda s: s if s.startswith("amazon-") else None,
        )
        assign_if_not_none(
            target=result,
            source=eni,
            spec="Attachment.InstanceOwnerId",
            transform=lambda s: s if s.startswith("amazon-") else None,
        )
        assign_if_not_none(target=result, source=eni, spec="Attachment.InstanceId", transform=lambda s: random_id("i-", 17)())
        assign_if_not_none(target=result, source=eni, spec="NetworkInterfaceId", transform=lambda s: random_id("eni-", 17)())

        results.append(result)
    return results


def get_only_unique_or_unknown(enis: list[dict]):
    unique_enis = []
    unique_services = set()

    for eni in enis:
        info = aws_eni_identifier.identify.identify_eni(eni)

        if service := info.get("svc"):
            if service not in unique_services:
                unique_services.add(service)
                unique_enis.append(eni)
        else:
            unique_enis.append(eni)

    return unique_enis


if __name__ == "__main__":
    with open("raw-enis.json", "r") as f:
        enis: list[dict] = json.load(f)["NetworkInterfaces"]

    anonymized_enis = anonimize(enis)

    with open("tests/assets/anonymized-enis.json", "w") as f:
        json.dump({"NetworkInterfaces": anonymized_enis}, f, indent=4)

    with open("tests/assets/unique-enis.json", "w") as f:
        json.dump(
            {"NetworkInterfaces": get_only_unique_or_unknown(anonymized_enis)},
            f,
            indent=4,
        )
