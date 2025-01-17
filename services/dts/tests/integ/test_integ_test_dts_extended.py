# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

import os
import json
import click
import pytest
import unittest
from tests import test_config_container
from tests import util

CASSETTE_LIBRARY_DIR = 'services/dts/tests/cassettes'


@pytest.fixture(autouse=True, scope='module')
def vcr_fixture(request):
    with test_config_container.create_vcr(cassette_library_dir=CASSETTE_LIBRARY_DIR).use_cassette('dts_integ_tests.yml'):
        yield


class IntegTestDTS(unittest.TestCase):
    class TestResult():
        Success = 1
        Skipped = 2
        Failed = 3

    def setUp(self):
        self.command_prefix = ["dts"]
        integ_compartment = os.environ["OCI_CLI_COMPARTMENT_ID"]
        integ_profile = "R1_LOCAL_AD1"
        integ_r1_cert_bundle_path = "/root/dts-oci-cli-env/dts-oci-cli-config/combined_r1.crt"
        integ_bucket = "abhaya_dts_bucket"
        self.config = {
            "$COMPARTMENT": integ_compartment,
            "$PROFILE": integ_profile,
            "$CERT_BUNDLE_PATH": integ_r1_cert_bundle_path,
            "$BUCKET": integ_bucket,
            "$JOB_ID": "NOT_POPULATED",
            "$APPLIANCE_LABEL": "NOT_POPULATED",
        }
        shipping_addr_with_required_fields = '{"zipcode": "94555", "country": "USA", "email": "dts@oracle.com", "care-of": "Oracle", "phone-number": "5101234567", "state-or-region": "CA", "addressee": "John Doe", "city-or-locality": "Santa Clara", "address1": "4100 Network Circle"}'
        shipping_addr_with_required_fields_with_updates = '{"zipcode": "94444", "country": "USA", "email": "dts_updated@oracle.com", "care-of": "Oracle-updated", "phone-number": "5101231234", "state-or-region": "CA", "addressee": "John DoeUpdated", "city-or-locality": "Santa Clara Updated", "address1": "4100 Network Circle Updated"}'

        self.commands = [
            {"verb": "list",
             "command_data":
                 ["job", "list", "--compartment-id", "$COMPARTMENT", "--profile", "$PROFILE",
                  "--cert-bundle", "$CERT_BUNDLE_PATH"]},
            {"verb": "create",
             "command_data":
                 ["job", "create",
                  "--compartment-id", "$COMPARTMENT", "--profile", "$PROFILE",
                  "--cert-bundle", "$CERT_BUNDLE_PATH",
                  "--bucket", "$BUCKET", "--display-name", "oci-cli-test-job-1",
                  "--device-type", "APPLIANCE"], "extract_from_output": {"id": "$JOB_ID"}},
            {"verb": "update",
             "command_data":
                 ["job", "update", "--job-id", "$JOB_ID",
                  "--profile", "$PROFILE", "--cert-bundle",
                  "$CERT_BUNDLE_PATH",
                  "--display-name", "oci-cli-test-job-2"]},
            {"verb": "create",
             "command_data":
                 ["appliance", "request", "--job-id", "$JOB_ID",
                  "--customer-shipping-address", shipping_addr_with_required_fields,
                  "--profile", "$PROFILE", "--cert-bundle",
                  "$CERT_BUNDLE_PATH"], "extract_from_output": {"label": "$APPLIANCE_LABEL"}},
            {"verb": "list",
             "command_data":
                 ["appliance", "list", "--job-id", "$JOB_ID",
                  "--profile", "$PROFILE", "--cert-bundle", "$CERT_BUNDLE_PATH"]},
            {"verb": "show",
             "command_data":
                 ["appliance", "show", "--job-id", "$JOB_ID", "--appliance-label", "$APPLIANCE_LABEL",
                  "--profile", "$PROFILE", "--cert-bundle", "$CERT_BUNDLE_PATH"]},
            {"verb": "update",
             "command_data":
                 ["appliance", "update-shipping-address", "--job-id", "$JOB_ID", "--appliance-label", "$APPLIANCE_LABEL",
                  "--customer-shipping-address", shipping_addr_with_required_fields_with_updates, "--force",
                  "--profile", "$PROFILE", "--cert-bundle", "$CERT_BUNDLE_PATH"]},
            {"verb": "delete",
             "command_data":
                 ["appliance", "delete", "--force", "--job-id", "$JOB_ID", "--appliance-label", "$APPLIANCE_LABEL",
                  "--profile", "$PROFILE", "--cert-bundle", "$CERT_BUNDLE_PATH"]},
            {"verb": "delete",
             "command_data":
                ["job", "delete", "--force", "--job-id", "$JOB_ID",
                 "--profile", "$PROFILE", "--cert-bundle", "$CERT_BUNDLE_PATH"]},
            {"verb": "verify",
             "command_data":
                ["job", "verify-upload-user-credentials", "--bucket", integ_bucket,
                 "--profile", "$PROFILE", "--cert-bundle", "$CERT_BUNDLE_PATH"]}
        ]

    def test_dts(self):
        success_count = 0
        failed_count = 0
        skipped_count = 0
        click.echo("")
        for command in self.commands:
            command_data = command["command_data"]
            for i, val in enumerate(command_data):
                if val in self.config:
                    command_data[i] = self.config[val]
            ret, j = self._execute(command_data)
            if ret == 0:
                success_count += 1
            else:
                failed_count += 1
                click.echo("command=%s, Error=%d, output=%s" % (command["verb"], ret, json.dumps(j, indent=2)))
                continue
            click.echo("%s-output=\n%s" % (command["verb"], json.dumps(j, indent=2)))
            try:
                kv = command["extract_from_output"]
            except Exception as e:
                kv = {}
            for k in kv:
                if j is not None:
                    self.config[kv[k]] = j["data"][k]
                    click.echo("Extracted from output:%s=%s" % (kv[k], j["data"][k]))

        click.echo("Tests: success=%d, failures=%d, skipped=%d" % (success_count, failed_count, skipped_count))

    def _execute(self, command):
        j_out = {}
        ret = 0
        try:
            command = self.command_prefix + command
            click.echo("command=%s" % (command))
            result = util.invoke_command(command)
            s = result.output
            print("Output=%s" % (s))
            if len(s) > 0:
                try:
                    j_out = json.loads(s)
                except Exception as e:
                    j_out = None
        except Exception as e:
            click.echo("_execute() Exception:%s" % (repr(e)))
            ret = -1
        finally:
            return ret, j_out
