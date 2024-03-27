#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Invoke tasks. To run a task, run ``$ invoke <COMMAND>``. To see a list of
commands, run ``$ invoke --list``.
"""

import glob
import logging
import os
import sys

from invoke import task

logging.getLogger("invoke").setLevel(logging.CRITICAL)

HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BIN_PATH = os.path.dirname(sys.executable)
bin_prefix = lambda cmd: os.path.join(BIN_PATH, cmd)
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 0))


@task(aliases=["flake8"])
def flake(ctx):
    ctx.run("flake8 .", echo=True)


@task(aliases=["autopep8"])
def autopep(ctx):
    ctx.run("autopep8 .", echo=True)


@task
def clean(ctx, verbose=False):
    ctx.run('find . -name "*.pyc" -delete', echo=True)


@task(aliases=["req"])
def requirements(ctx, dev=False):
    """Install python dependencies.

    Examples:
        invoke requirements
    """

    req_file = os.path.join(HERE, "requirements.txt")
    cmd = bin_prefix("pip install --exists-action w --upgrade -r {} ".format(req_file))
    ctx.run(cmd, echo=True)


@task
def test_module_wo_exit(ctx, module=None, params=None):
    """Helper for running tests."""
    import pytest

    if params is None:
        params = []

    args = [
        "-s",
        "-v",
        "--tb=short",
        "--write_files",
        "false",
        "--exclude_best_practice",
        "true",
    ]
    for e in [module, params]:
        if e:
            args.extend([e] if isinstance(e, str) else e)

    print(">>> pytest args: {}".format(args))
    retcode = pytest.main(args)
    return retcode


@task
def test_module(ctx, module=None, params=None):
    """Helper for running tests."""
    retcode = test_module_wo_exit(ctx, module, params)
    sys.exit(retcode)


@task
def test_ember_accessibility(ctx):
    """Run the accessibility tests for Ember pages on the browser defined by TEST_BUILD.
    This task will be invoked after 'ember-osf-web' has been deployed to any testing
    environment.   In order to be included in this test run the test must have the
    pytest marker 'ember_page'.
    """
    test_with_retries(
        ctx, "Ember Pages", _get_test_file_list(), module=["-m", "ember_page"]
    )


@task
def test_legacy_accessibility(ctx):
    """Run the accessibility tests for Legacy pages on the browser defined by TEST_BUILD.
    This task will be invoked after 'osf.io' has been deployed to any testing
    environment.   In order to be included in this test run the test must have the
    pytest marker 'legacy_page'.
    """
    test_with_retries(
        ctx, "Legacy Pages", _get_test_file_list(), module=["-m", "legacy_page"]
    )


@task
def test_preprints_accessibility(ctx):
    """Run the accessibility test for Preprints on the browser defined by TEST_BUILD.
    This task will be invoked after 'ember-osf-preprints' has been deployed to any
    testing environment.
    """
    file_list = ["tests/test_a11y_preprints.py"]
    test_with_retries(ctx, "Preprints", file_list)


@task
def test_cas_accessibility(ctx):
    """Run the accessibility test for CAS on the browser defined by TEST_BUILD.
    This task will be invoked after 'osf-cas' has been deployed to any testing
    environment.
    """
    file_list = ["tests/test_a11y_cas.py"]
    test_with_retries(ctx, "CAS", file_list)


def _get_test_file_list():
    all_test_files = glob.glob("tests/test_*.py")
    all_test_files.sort()
    return all_test_files


@task
def test_with_retries(ctx, partition_name, file_list, module=None):
    """Run group of tests on the browser defined by TEST_BUILD."""
    flake(ctx)

    print(
        '>>> Testing {} modules in "/tests/" in {}'.format(
            partition_name, os.environ["TEST_BUILD"]
        )
    )
    print(">>> File list for {} is: {}".format(partition_name, file_list))
    retcode = test_module_wo_exit(ctx, params=file_list, module=module)

    if retcode != 1:
        sys.exit(retcode)

    file_list = ["--last-failed", "--last-failed-no-failures", "none"] + file_list

    for i in range(1, MAX_RETRIES + 1):
        print(
            '>>> Retesting {} failures, iteration {}, in "/test/" '
            "in {}".format(partition_name, i, os.environ["TEST_BUILD"])
        )
        retcode = test_module_wo_exit(ctx, params=file_list, module=module)

        if retcode != 1:
            break

    sys.exit(retcode)
