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

    return info


# z = {"Attachment.InstanceOwnerId" "InterfaceType"}
# if eni_object.attachment_owner_id is not None:
#     if eni_object.attachment_owner_id == 'amazon-rds' or eni_object.description.startswith('Network interface for DBProxy '):
#         return RDS(info)
#     if eni_object.attachment_owner_id == 'amazon-elb':
#         return ELB(info)
#     if eni_object.attachment_owner_id == 'amazon-aws' and eni_object.type == 'lambda':
#         return Lambda(info)
#     if eni_object.attachment_owner_id == 'amazon-aws' and eni_object.type == 'vpc_endpoint':
#         return VPCElasticNetworkInterface(info)
#     if eni_object.attachment_owner_id == 'amazon-aws' and eni_object.type == 'nat_gateway':
#         return NATGateway(info)
#     if eni_object.attachment_owner_id == 'amazon-aws' and eni_object.type == 'global_accelerator_managed':
#         return GlobalAccelerator(info)

#     if eni_object.attachment_owner_id == 'amazon-aws' and eni_object.description.startswith('EFS mount target for '):
#         return ElasticFileSystemEFSFileSystem(info)
