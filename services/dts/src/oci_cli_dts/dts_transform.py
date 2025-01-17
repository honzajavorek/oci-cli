# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

from __future__ import print_function

from oci_cli import cli_util


class DTS_Transform(object):
    def __init__(self):
        pass

    @staticmethod
    def transform(command_help_override_list=[],
                  group_help_override_list=[],
                  rename_command_list=[],
                  relocate_command_list=[],
                  pop_command_list=[]):
        for item in command_help_override_list:
            cli_util.override_command_short_help_and_help(item["command"], item["help_text"])
        for item in group_help_override_list:
            item["group"].help = item["help_text"]
            item["group"].short_help = item["short_help_text"]
        for item in rename_command_list:
            cli_util.rename_command(item["group"], item["old"], item["new"])
        for item in relocate_command_list:
            item["group"].add_command(item["command"])
        for item in pop_command_list:
            item["group"].commands.pop(item["command"])
