# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

from __future__ import print_function
import click
import oci  # noqa: F401
import six  # noqa: F401
import sys  # noqa: F401
from oci_cli import cli_constants  # noqa: F401
from oci_cli import cli_util
from oci_cli import json_skeleton_utils
from oci_cli import custom_types  # noqa: F401
from oci_cli.aliasing import CommandGroupWithAlias
from services.dts.src.oci_cli_dts.generated import dts_service_cli


@click.command(cli_util.override('transfer_job_root_group.command_name', 'transfer-job'), cls=CommandGroupWithAlias, help=cli_util.override('transfer_job_root_group.help', """A description of the DTS API"""), short_help=cli_util.override('transfer_job_root_group.short_help', """DTS API"""))
@cli_util.help_option_group
def transfer_job_root_group():
    pass


@click.command(cli_util.override('detach_devices_details_group.command_name', 'detach-devices-details'), cls=CommandGroupWithAlias, help="""""")
@cli_util.help_option_group
def detach_devices_details_group():
    pass


@click.command(cli_util.override('transfer_job_group.command_name', 'transfer-job'), cls=CommandGroupWithAlias, help="""""")
@cli_util.help_option_group
def transfer_job_group():
    pass


dts_service_cli.dts_service_group.add_command(transfer_job_root_group)
transfer_job_root_group.add_command(detach_devices_details_group)
transfer_job_root_group.add_command(transfer_job_group)


@detach_devices_details_group.command(name=cli_util.override('change_transfer_job_compartment.command_name', 'change-compartment'), help=u"""Moves a TransferJob into a different compartment.""")
@cli_util.option('--transfer-job-id', required=True, help=u"""ID of the Transfer Job""")
@cli_util.option('--compartment-id', required=True, help=u"""The [OCID]  of the compartment into which the resources should be moved.""")
@cli_util.option('--if-match', help=u"""The entity tag to match. Optional, if set, the update will be successful only if the object's tag matches the tag specified in the request.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def change_transfer_job_compartment(ctx, from_json, transfer_job_id, compartment_id, if_match):

    if isinstance(transfer_job_id, six.string_types) and len(transfer_job_id.strip()) == 0:
        raise click.UsageError('Parameter --transfer-job-id cannot be whitespace or empty string')

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}
    details['compartmentId'] = compartment_id

    client = cli_util.build_client('transfer_job', ctx)
    result = client.change_transfer_job_compartment(
        transfer_job_id=transfer_job_id,
        change_transfer_job_compartment_details=details,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@transfer_job_group.command(name=cli_util.override('create_transfer_job.command_name', 'create'), help=u"""Create a new Transfer Job that corresponds with customer's logical dataset e.g. a DB or a filesystem.""")
@cli_util.option('--compartment-id', help=u"""""")
@cli_util.option('--upload-bucket-name', help=u"""""")
@cli_util.option('--display-name', help=u"""""")
@cli_util.option('--device-type', type=custom_types.CliCaseInsensitiveChoice(["DISK", "APPLIANCE"]), help=u"""""")
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{\"bar-key\": \"value\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Usage of predefined tag keys. These predefined keys are scoped to namespaces. Example: `{\"foo-namespace\": {\"bar-key\": \"foo-value\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["INITIATED", "PREPARING", "ACTIVE", "DELETED", "CLOSED"]), help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'freeform-tags': {'module': 'dts', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'dts', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'freeform-tags': {'module': 'dts', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'dts', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'dts', 'class': 'TransferJob'})
@cli_util.wrap_exceptions
def create_transfer_job(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, compartment_id, upload_bucket_name, display_name, device_type, freeform_tags, defined_tags):

    kwargs = {}

    details = {}

    if compartment_id is not None:
        details['compartmentId'] = compartment_id

    if upload_bucket_name is not None:
        details['uploadBucketName'] = upload_bucket_name

    if display_name is not None:
        details['displayName'] = display_name

    if device_type is not None:
        details['deviceType'] = device_type

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    client = cli_util.build_client('transfer_job', ctx)
    result = client.create_transfer_job(
        create_transfer_job_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_transfer_job') and callable(getattr(client, 'get_transfer_job')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_transfer_job(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@transfer_job_group.command(name=cli_util.override('delete_transfer_job.command_name', 'delete'), help=u"""deletes a transfer job""")
@cli_util.option('--id', required=True, help=u"""ID of the Transfer Job""")
@cli_util.confirm_delete_option
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["INITIATED", "PREPARING", "ACTIVE", "DELETED", "CLOSED"]), help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def delete_transfer_job(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, id):

    if isinstance(id, six.string_types) and len(id.strip()) == 0:
        raise click.UsageError('Parameter --id cannot be whitespace or empty string')

    kwargs = {}
    client = cli_util.build_client('transfer_job', ctx)
    result = client.delete_transfer_job(
        id=id,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_transfer_job') and callable(getattr(client, 'get_transfer_job')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                oci.wait_until(client, client.get_transfer_job(id), 'lifecycle_state', wait_for_state, succeed_on_not_found=True, **wait_period_kwargs)
            except oci.exceptions.ServiceError as e:
                # We make an initial service call so we can pass the result to oci.wait_until(), however if we are waiting on the
                # outcome of a delete operation it is possible that the resource is already gone and so the initial service call
                # will result in an exception that reflects a HTTP 404. In this case, we can exit with success (rather than raising
                # the exception) since this would have been the behaviour in the waiter anyway (as for delete we provide the argument
                # succeed_on_not_found=True to the waiter).
                #
                # Any non-404 should still result in the exception being thrown.
                if e.status == 404:
                    pass
                else:
                    raise
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Please retrieve the resource to find its current state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@transfer_job_group.command(name=cli_util.override('get_transfer_job.command_name', 'get'), help=u"""Describes a transfer job in detail""")
@cli_util.option('--id', required=True, help=u"""OCID of the Transfer Job""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'dts', 'class': 'TransferJob'})
@cli_util.wrap_exceptions
def get_transfer_job(ctx, from_json, id):

    if isinstance(id, six.string_types) and len(id.strip()) == 0:
        raise click.UsageError('Parameter --id cannot be whitespace or empty string')

    kwargs = {}
    client = cli_util.build_client('transfer_job', ctx)
    result = client.get_transfer_job(
        id=id,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@transfer_job_group.command(name=cli_util.override('list_transfer_jobs.command_name', 'list'), help=u"""Lists Transfer Jobs in a given compartment""")
@cli_util.option('--compartment-id', required=True, help=u"""compartment id""")
@cli_util.option('--lifecycle-state', type=custom_types.CliCaseInsensitiveChoice(["INITIATED", "PREPARING", "ACTIVE", "DELETED", "CLOSED"]), help=u"""filtering by lifecycleState""")
@cli_util.option('--display-name', help=u"""filtering by displayName""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'dts', 'class': 'list[TransferJobSummary]'})
@cli_util.wrap_exceptions
def list_transfer_jobs(ctx, from_json, all_pages, compartment_id, lifecycle_state, display_name):

    kwargs = {}
    if lifecycle_state is not None:
        kwargs['lifecycle_state'] = lifecycle_state
    if display_name is not None:
        kwargs['display_name'] = display_name
    client = cli_util.build_client('transfer_job', ctx)
    result = client.list_transfer_jobs(
        compartment_id=compartment_id,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@transfer_job_group.command(name=cli_util.override('update_transfer_job.command_name', 'update'), help=u"""Updates a Transfer Job that corresponds with customer's logical dataset e.g. a DB or a filesystem.""")
@cli_util.option('--id', required=True, help=u"""ID of the Transfer Job""")
@cli_util.option('--lifecycle-state', type=custom_types.CliCaseInsensitiveChoice(["CLOSED"]), help=u"""""")
@cli_util.option('--display-name', help=u"""""")
@cli_util.option('--device-type', type=custom_types.CliCaseInsensitiveChoice(["DISK", "APPLIANCE"]), help=u"""""")
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{\"bar-key\": \"value\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Usage of predefined tag keys. These predefined keys are scoped to namespaces. Example: `{\"foo-namespace\": {\"bar-key\": \"foo-value\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--if-match', help=u"""The entity tag to match. Optional, if set, the update will be successful only if the object's tag matches the tag specified in the request.""")
@cli_util.option('--force', help="""Perform update without prompting for confirmation.""", is_flag=True)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["INITIATED", "PREPARING", "ACTIVE", "DELETED", "CLOSED"]), help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'freeform-tags': {'module': 'dts', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'dts', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'freeform-tags': {'module': 'dts', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'dts', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'dts', 'class': 'TransferJob'})
@cli_util.wrap_exceptions
def update_transfer_job(ctx, from_json, force, wait_for_state, max_wait_seconds, wait_interval_seconds, id, lifecycle_state, display_name, device_type, freeform_tags, defined_tags, if_match):

    if isinstance(id, six.string_types) and len(id.strip()) == 0:
        raise click.UsageError('Parameter --id cannot be whitespace or empty string')
    if not force:
        if freeform_tags or defined_tags:
            if not click.confirm("WARNING: Updates to freeform-tags and defined-tags will replace any existing values. Are you sure you want to continue?"):
                ctx.abort()

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match

    details = {}

    if lifecycle_state is not None:
        details['lifecycleState'] = lifecycle_state

    if display_name is not None:
        details['displayName'] = display_name

    if device_type is not None:
        details['deviceType'] = device_type

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    client = cli_util.build_client('transfer_job', ctx)
    result = client.update_transfer_job(
        id=id,
        update_transfer_job_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_transfer_job') and callable(getattr(client, 'get_transfer_job')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_transfer_job(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)
