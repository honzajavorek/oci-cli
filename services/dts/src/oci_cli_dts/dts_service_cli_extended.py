# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

from __future__ import print_function

from services.dts.src.oci_cli_dts.generated import dts_service_cli
from services.dts.src.oci_cli_transfer_job.generated import transferjob_cli
from services.dts.src.oci_cli_transfer_appliance.generated import transferappliance_cli
from services.dts.src.oci_cli_transfer_appliance_entitlement.generated import transferapplianceentitlement_cli
from services.dts.src.oci_cli_transfer_device.generated import transferdevice_cli
from services.dts.src.oci_cli_transfer_package.generated import transferpackage_cli
from services.dts.src.oci_cli_shipping_vendors.generated import shippingvendors_cli

from services.dts.src.oci_cli_dts.dts_transform import DTS_Transform

# COMMAND HELP OVERRIDES ####
command_help_override_list = [
    # Job
    {"command": transferjob_cli.create_transfer_job,
        "help_text": "Creates a new transfer disk or appliance job."},
    {"command": transferjob_cli.get_transfer_job,
        "help_text": "Shows the transfer disk or appliance job details."},
    {"command": transferjob_cli.update_transfer_job,
        "help_text": "Updates the transfer disk or appliance job details."},
    {"command": transferjob_cli.delete_transfer_job,
        "help_text": "Deletes the transfer disk or appliance job."},
    {"command": transferjob_cli.list_transfer_jobs,
        "help_text": "Lists all transfer disk or appliance jobs."},
]
#

# GROUP HELP STRING OVERRIDES #####
group_help_override_list = [
    {"group": dts_service_cli.dts_service_group,
        "help_text": "Transfer disk or appliance job operations",
        "short_help_text": "Data Transfer Service"},

    {"group": transferjob_cli.transfer_job_root_group,
        "help_text": "Transfer disk or appliance job operations",
        "short_help_text": "Transfer disk or appliance job operations"},

    {"group": transferappliance_cli.transfer_appliance_root_group,
        "help_text": "Transfer appliance operations",
        "short_help_text": "Transfer appliance operations"},


]
#


# RENAME COMMANDS #####
rename_command_list = [
    {"group": dts_service_cli.dts_service_group, "old": transferjob_cli.transfer_job_root_group, "new": "job"},
    {"group": dts_service_cli.dts_service_group, "old": transferappliance_cli.transfer_appliance_root_group, "new": "appliance"},

    {"group": transferjob_cli.transfer_job_root_group, "old": transferjob_cli.get_transfer_job, "new": "show"},

    {"group": transferappliance_cli.transfer_appliance_root_group, "old": transferappliance_cli.get_transfer_appliance, "new": "show"},
    {"group": transferappliance_cli.transfer_appliance_root_group, "old": transferappliance_cli.create_transfer_appliance, "new": "request"},
    {"group": transferappliance_cli.transfer_appliance_encryption_passphrase_group, "old": transferappliance_cli.get_transfer_appliance_encryption_passphrase, "new": "get-passphrase"},
    {"group": transferappliance_cli.transfer_appliance_root_group, "old": transferappliance_cli.list_transfer_appliances, "new": "list"},

]
#


# RELOCATE COMMANDS ####
relocate_command_list = [
    # dts job commands
    {"group": transferjob_cli.transfer_job_root_group, "command": transferjob_cli.create_transfer_job},
    {"group": transferjob_cli.transfer_job_root_group, "command": transferjob_cli.delete_transfer_job},
    {"group": transferjob_cli.transfer_job_root_group, "command": transferjob_cli.get_transfer_job},
    {"group": transferjob_cli.transfer_job_root_group, "command": transferjob_cli.list_transfer_jobs},
    {"group": transferjob_cli.transfer_job_root_group, "command": transferjob_cli.update_transfer_job},

    # dts appliance commands
    {"group": transferappliance_cli.transfer_appliance_root_group, "command": transferappliance_cli.create_transfer_appliance},
    {"group": transferappliance_cli.transfer_appliance_root_group, "command": transferappliance_cli.delete_transfer_appliance},
    {"group": transferappliance_cli.transfer_appliance_root_group, "command": transferappliance_cli.list_transfer_appliances},
    {"group": transferappliance_cli.transfer_appliance_root_group, "command": transferappliance_cli.get_transfer_appliance},
    {"group": transferappliance_cli.transfer_appliance_root_group, "command": transferappliance_cli.get_transfer_appliance_encryption_passphrase},

    # transfer-appliance-entitlement
    # Entitlement is made out of scope since it is going through spec review and backend code is turned off.
    #    This will be turned on in a subsequent release.
    # {"group": transferapplianceentitlement_cli.transfer_appliance_entitlement_root_group,
    #  "command": transferapplianceentitlement_cli.create_transfer_appliance_entitlement},
    # {"group": transferapplianceentitlement_cli.transfer_appliance_entitlement_root_group,
    #  "command": transferapplianceentitlement_cli.get_transfer_appliance_entitlement},
]
#

# POP COMMANDS #######
pop_command_list = [
    # dts
    {"group": dts_service_cli.dts_service_group, "command": transferdevice_cli.transfer_device_group.name},
    {"group": dts_service_cli.dts_service_group, "command": transferpackage_cli.transfer_package_group.name},
    {"group": dts_service_cli.dts_service_group, "command": shippingvendors_cli.shipping_vendors_group.name},

    # dts job
    {"group": transferjob_cli.transfer_job_root_group, "command": transferjob_cli.transfer_job_group.name},

    # dts appliance
    {"group": transferappliance_cli.transfer_appliance_root_group, "command": transferappliance_cli.transfer_appliance_group.name},
    {"group": transferappliance_cli.transfer_appliance_root_group, "command": transferappliance_cli.transfer_appliance_encryption_passphrase_group.name},
    {"group": transferappliance_cli.transfer_appliance_root_group, "command": transferappliance_cli.transfer_appliance_certificate_group.name},
    {"group": transferappliance_cli.transfer_appliance_root_group, "command": transferappliance_cli.transfer_appliance_public_key_group.name},

    # dts appliance entitlement
    # Entitlement command: Turn this on and delete the lines right below making entitlement command visible once the spec review completes and backend code is turned on.
    # {"group": transferapplianceentitlement_cli.transfer_appliance_entitlement_root_group,
    # "command": transferapplianceentitlement_cli.transfer_appliance_entitlement_group.name},
    {"group": dts_service_cli.dts_service_group,
        "command": transferapplianceentitlement_cli.transfer_appliance_entitlement_group.name},
]
####

DTS_Transform.transform(command_help_override_list=command_help_override_list,
                        group_help_override_list=group_help_override_list,
                        rename_command_list=rename_command_list,
                        relocate_command_list=relocate_command_list,
                        pop_command_list=pop_command_list)
