from glom import glom

import aws_eni_identifier as aei


def identify_eni(eni: dict) -> dict:
    info = glom(eni, {"eni": "NetworkInterfaceId"}, default=None)
    if not isinstance(info, dict):
        return {}

    if id := glom(eni, "Attachment.InstanceId", default=None):
        extra = {"svc": "ec2", "name": id}
        info |= extra

    elif dscr := eni.get("Description"):
        if _info := aei.extract_description_info(dscr):
            info |= _info
    # TODO: "RequesterId", "Attachment.InstanceOwnerId",
    # TODO: "InterfaceType"
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_network_interfaces
    # api_gateway_managed | aws_codestar_connections_managed | branch | efa | gateway_load_balancer | gateway_load_balancer_endpoint | global_accelerator_managed | interface | iot_rules_managed | lambda | load_balancer | nat_gateway | network_load_balancer | quicksight | transit_gateway | trunk | vpc_endpoint
    return info
