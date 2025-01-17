# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.


# A note on the tests.
# These tests are for asserting the command line syntax.
# These tests do NOT need to connect to the control plane.
# Tests:
# test-1: Run command without any arguments.
#      Assert that the output is reporting missing params for all REQUIRED params.
# test-2: Supply all required args
#     Assert that we get a 404 or 401. config.unittest has valid cred for R1 so that it connects.
# test-3: Supply all required AND optional params
#     Assert the same as test-2.
#     This tests that the command accepts all optional params.

import enum
import json
import click
import pytest
import unittest
from tests import test_config_container
from tests import util

import mock
from oci.response import Response
from oci.request import Request
from services.dts.src.oci_cli_dts.physical_appliance_control_plane.client.models.nfs_dataset_info import NfsDatasetInfo

CASSETTE_LIBRARY_DIR = 'services/dts/tests/cassettes'


@pytest.fixture(autouse=True, scope='module')
def vcr_fixture(request):
    with test_config_container.create_vcr(cassette_library_dir=CASSETTE_LIBRARY_DIR).use_cassette('dts_unit_tests.yml'):
        yield


class UnitTestDTS(unittest.TestCase):
    class TestResult(enum.Enum):
        Success = 1
        Skipped = 2
        Failed = 3

    class TestType(enum.Enum):
        NoArgs = "NoArgs"
        OnlyRequiredArgs = "OnlyRequiredArgs"
        AllArgs = "AllArgs"
        GenFullCommandFromJson = "GenFullCommandFromJson"

    Missing_params_Text = "Error: Missing option(s)"

    def setUp(self):
        self.test_specific_set = {}  # When empty, all tests are run.
        # self.test_specific_set = {"appliance":["request"]}

        self.specific_arg_values = {"profile": "DEFAULT", "device-type": "APPLIANCE",
                                    "wait": None, "rw": "True", "world": "True",
                                    "test_defined_tag": '{"string1": "string", "string2": "string"}'}
        self.complex_data_defs = {
            "customer-shipping-address": {
                "required_params": ["addressee", "care-of", "address1", "city-or-locality", "state-or-region",
                                    "country", "zipcode", "phone-number", "email"],
                "optional_params": ["address2", "address3", "address4"]
            },
            "freeform-tags": {
                "required_params": ["string1"],
                "optional_params": []
            },
            "defined-tags": {
                "required_params": ["test_defined_tag"],
                "optional_params": []
            },

        }

        self.job_subcommands = [
            {"sub_command": "create",
             "required_params": ["compartment-id", "bucket", "display-name", "device-type"],
             "optional_params": ["defined-tags", "freeform-tags", "profile"]},
            {"sub_command": "show",
             "required_params": ["job-id"],
             "optional_params": []},
            {"sub_command": "update",
             "required_params": ["job-id"],
             "optional_params": ["defined-tags", "freeform-tags", "display-name"]},
            {"sub_command": "delete",
             "required_params": ["job-id"],
             "optional_params": []},
            {"sub_command": "close",
             "required_params": ["job-id"],
             "optional_params": []},
            {"sub_command": "verify-upload-user-credentials",
             "required_params": ["bucket"],
             "optional_params": []},
        ]
        self.appliance_subcommands = [
            {"sub_command": "request",
             "required_params": ["job-id", "customer-shipping-address"],
             "optional_params": []},
            {"sub_command": "show",
             "required_params": ["job-id", "appliance-label"],
             "optional_params": []},
            {"sub_command": "list",
             "required_params": ["job-id"],
             "optional_params": []},
            {"sub_command": "get-passphrase",
             "required_params": ["job-id", "appliance-label"],
             "optional_params": []},
            {"sub_command": "never-receive",
             "required_params": ["job-id", "appliance-label"],
             "optional_params": []},
            {"sub_command": "cancel",
             "required_params": ["job-id", "appliance-label"],
             "optional_params": []},
            {"sub_command": "delete",
             "required_params": ["job-id", "appliance-label"],
             "optional_params": []},
            {"sub_command": "update-shipping-address",
             "required_params": ["job-id", "appliance-label", "customer-shipping-address"],
             "optional_params": []}
        ]
        self.pa_subcommands = [
            {"sub_command": "initialize-authentication",
             "required_params": ["job-id", "appliance-label", "appliance-cert-fingerprint", "appliance-ip"],
             "optional_params": ["appliance-profile", "appliance-port", "access-token", "profile"]},
            {"sub_command": "list",
             "required_params": [],
             "optional_params": []},
            {"sub_command": "configure-encryption",
             "required_params": ["job-id", "appliance-label"],
             "optional_params": ["appliance-profile"]},
            {"sub_command": "show",
             "required_params": [],
             "optional_params": ["appliance-profile"]},
            {"sub_command": "unlock",
             "required_params": ["job-id", "appliance-label"],
             "optional_params": ["appliance-profile"]},
            {"sub_command": "finalize",
             "required_params": ["job-id", "appliance-label"],
             "optional_params": ["appliance-profile", "profile"],
             "methods_to_side_effect": {}},
        ]
        nfs_datasets = [{'name': '123', 'state': NfsDatasetInfo.STATE_ACTIVE,
                         'dataset_type': NfsDatasetInfo.DATASET_TYPE_NFS, 'nfs_export_details': None}]
        self.nfs_ds_subcommands = [
            {"sub_command": "create",
             "required_params": ["name"],
             "optional_params": ["rw", "world", "ip", "subnet-mask-length", "appliance-profile"]},
            {"sub_command": "set-export",
             "required_params": ["name", "rw", "world"],
             "optional_params": ["ip", "subnet-mask-length", "appliance-profile"]},
            {"sub_command": "show",
             "required_params": ["name"],
             "optional_params": ["appliance-profile"]},
            {"sub_command": "list",
             "required_params": [],
             "optional_params": ["appliance-profile"]},
            {"sub_command": "delete",
             "required_params": ["name"],
             "optional_params": ["appliance-profile"]},
            {"sub_command": "activate",
             "required_params": ["name"],
             "optional_params": ["rw", "world", "ip", "subnet-mask-length", "appliance-profile"],
             "methods_to_side_effect": {"mock_nfs_dataset_client": {"list_nfs_datasets": (200, {}, nfs_datasets)}}},
            {"sub_command": "deactivate",
             "required_params": ["name"],
             "optional_params": ["appliance-profile"]},
            {"sub_command": "seal",
             "required_params": [],
             "optional_params": ["name", "appliance-profile"],
             "methods_to_side_effect": {"mock_nfs_dataset_client": {"list_nfs_datasets": (200, {}, nfs_datasets)}}},
            {"sub_command": "reopen",
             "required_params": ["name"],
             "optional_params": ["appliance-profile"]},
            {"sub_command": "seal-status",
             "required_params": ["name"],
             "optional_params": ["appliance-profile"]},
            {"sub_command": "get-seal-manifest",
             "required_params": ["name", "output-file"],
             "optional_params": ["appliance-profile"]},
        ]
        self.entitlement_subcommands = [
            {"sub_command": "create",
             "required_params": ["tenant-id", "name", "email"],
             "optional_params": ["profile"]},
            {"sub_command": "get",
             "required_params": ["tenant-id"],
             "optional_params": ["profile"]},
        ]
        self.command_defs = [
            {"command": "job", "sub_commands": self.job_subcommands},
            {"command": "appliance", "sub_commands": self.appliance_subcommands},
            {"command": "physical-appliance", "sub_commands": self.pa_subcommands},
            {"command": "nfs-dataset", "sub_commands": self.nfs_ds_subcommands}
            # Uncomment the line below when entitlement command is in scope.
            # {"command": "transfer-appliance-entitlement", "sub_commands": self.entitlement_subcommands},
        ]

        self.success_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.failure_msg_list = []

    # For each sub-command, test that
    #       - CLI errors when any of the Required params is not supplied.
    #       - CLI accepts all Required params
    #       - CLI accepts all Optional params
    @mock.patch('services.dts.src.oci_cli_dts.nfsdataset_cli_extended.write_to_file')
    @mock.patch('services.dts.src.oci_cli_dts.nfsdataset_cli_extended.create_nfs_dataset_client')
    @mock.patch('services.dts.src.oci_cli_dts.physicalappliance_cli_extended.create_appliance_client')
    @mock.patch('services.dts.src.oci_cli_dts.physicalappliance_cli_extended.create_init_auth')
    @mock.patch('click.prompt', return_value=True)
    @mock.patch('oci_cli.cli_util.build_client')
    def test_dts(self, mock_client, mock_prompt, mock_init_auth, mock_appliance_client, mock_nfs_dataset_client,
                 mock_write_to_file):
        click.echo("")
        for command_def in self.command_defs:
            command = command_def["command"]
            specific_sub_command_set = self._sub_command_list_in_specific_test_set(command)
            if specific_sub_command_set is None:
                click.echo("Skipping command=%s; Not in test_specific_set;" % (command))
                self.skipped_count += 1
                continue
            for sub_command_def in command_def["sub_commands"]:
                if len(specific_sub_command_set) == 0 or sub_command_def["sub_command"] in specific_sub_command_set:
                    if 'methods_to_side_effect' in sub_command_def.keys():
                        # The key is the mock object name and the value is a dict of the side effects
                        for key, value in sub_command_def['methods_to_side_effect'].items():
                            # k is the method to side effect and v is the tuple of {status, headers, data}
                            for k, v in value.items():
                                def method_side_effect(**kwargs):
                                    return Response(v[0], v[1], v[2], Request("mock.method", "mock.url"))
                                exec("{}.return_value.{}.side_effect = method_side_effect".format(key, k)) in globals(), locals()
                    self._execute_subcommand(command, sub_command_def)
                else:
                    click.echo("Skipping command::sub-command=%s::%s; Not in test_specific_set;" % (command, sub_command_def["sub_command"]))
                    self.skipped_count += 1
                    continue

        click.echo("Consolidated-ErrorList=")
        for item in self.failure_msg_list:
            click.echo(item)
        click.echo("Tests: success=%d, failures=%d, skipped=%d" % (self.success_count, self.failed_count, self.skipped_count))

    def _sub_command_list_in_specific_test_set(self, command):
        if len(self.test_specific_set) == 0:
            return []
        else:
            if command in self.test_specific_set:
                return self.test_specific_set[command]
            else:
                return None

    def _execute_subcommand(self, command, sub_command_def):
        click.echo("command=%s,sub_command=%s" % (command, sub_command_def["sub_command"]))
        try:
            if sub_command_def["skip"].upper() == "TRUE":
                click.echo("Skipping...")
                self.skipped_count += 1
                return
        except Exception as e:
            pass
        # For focused testing. TODO: Promote to an env variable.
        specific_test_type = None
        # specific_test_type = self.TestType.OnlyRequiredArgs
        for test_type in self.TestType:
            if specific_test_type is not None and specific_test_type != test_type:
                continue
            c_list = self._generate_command_list(command, sub_command_def, test_type)
            if len(c_list) == 3 and sub_command_def["sub_command"] == "unlock":
                continue
            click.echo(c_list)
            result = util.invoke_command(c_list)
            ret = self._validate_result(command, result, sub_command_def, test_type)
            if ret == self.TestResult.Success:
                self.success_count += 1
            else:
                self.failed_count += 1

    def _generate_command_list(self, command, sub_command_def, test_type):
        # click.echo("command=%s,sub_command=%s::::%s" % (command, sub_command_def["sub_command"], test_type))
        c_list = ["dts", command, sub_command_def["sub_command"]]
        if (test_type == self.TestType.NoArgs):
            return c_list

        if 'update' in sub_command_def["sub_command"] or 'delete' in sub_command_def["sub_command"]\
                and command not in ['physical-appliance', 'nfs-dataset']:
            c_list.append("--force")
        c_arg_list = []
        if (test_type == self.TestType.OnlyRequiredArgs):
            c_arg_list += sub_command_def["required_params"]
        elif test_type == self.TestType.AllArgs:
            c_arg_list += sub_command_def["required_params"] + sub_command_def["optional_params"]
        elif test_type == self.TestType.GenFullCommandFromJson:
            c_list += ["--generate-full-command-json-input"]
        else:
            click.echo("_generate_command_list:Uncoded TestType=%s" % (test_type))
            return None
        c_list += self._add_args(c_arg_list, test_type)
        return c_list

    def _add_args(self, arg_list, test_type):

        new_arg_list = []
        for item in arg_list:
            s = ""
            new_arg_list.append("--" + item)
            if item in self.specific_arg_values:
                s = self.specific_arg_values[item]
            elif item in self.complex_data_defs:
                j = {}
                complex_data_args = self.complex_data_defs[item]
                if test_type == self.TestType.OnlyRequiredArgs or test_type == self.TestType.AllArgs:
                    for arg in complex_data_args["required_params"]:
                        if arg in self.specific_arg_values:
                            j[arg] = json.loads(self.specific_arg_values[arg])
                        else:
                            j[arg] = "456"
                if test_type == self.TestType.AllArgs:
                    for arg in complex_data_args["optional_params"]:
                        if arg in self.specific_arg_values:
                            j[arg] = json.loads(self.specific_arg_values[arg])
                        else:
                            j[arg] = "789"
                s = json.dumps(j)
            else:
                s = "123"
            if s is not None:
                new_arg_list.append(s)
        return new_arg_list

    def _print_error(self, command, sub_command, s):
        err = "command=%s,sub_command=%s,Error=%s\n" % (command, sub_command, s)
        click.echo(err)
        self.failure_msg_list.append(err)

    def _validate_result(self, command, result, sub_command_def, test_type):
        required_params = sub_command_def["required_params"]
        if test_type == self.TestType.NoArgs:
            cmd_result = UnitTestDTS.TestResult.Success
            if len(required_params) and self.Missing_params_Text not in result.output:
                self._print_error(command, sub_command_def["sub_command"], "Spec issue: %s need to be marked as Required." % (required_params))
                return UnitTestDTS.TestResult.Failed

            msg = ""
            for r_p in required_params:
                s = "--" + r_p

                try:
                    if s not in result.output:
                        msg += r_p + ","
                except Exception as e:
                    self._print_error(command, sub_command_def["sub_command"], "result does not carry field output: %s" % (result))
            if len(msg) > 0:
                msg = "Spec issue: %s need to be marked as Required." % (msg)
                self._print_error(command, sub_command_def["sub_command"], msg)
                cmd_result = UnitTestDTS.TestResult.Failed
            return cmd_result
        elif test_type == self.TestType.AllArgs or test_type == self.TestType.OnlyRequiredArgs:
            if result.exception is None:
                return UnitTestDTS.TestResult.Success
            else:
                self._print_error(
                    command, sub_command_def["sub_command"], "Incorrect result:**#%s#**" % result.output_bytes)
                return UnitTestDTS.TestResult.Failed
        elif test_type == self.TestType.GenFullCommandFromJson:
            if "Error:" in result.output:
                self._print_error(command, sub_command_def["sub_command"], "Incorrect result:**#%s#**" % result.output)
                return UnitTestDTS.TestResult.Failed
            else:
                return UnitTestDTS.TestResult.Success
