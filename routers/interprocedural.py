from flask import Blueprint, request
import subprocess

blueprint = Blueprint("interprocedural", __name__)


def get_safe_command(req):
    return "ls"


def get_vul_command(req):
    return req.args.get('key')


def execute_command(command):
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/ip/safe")
def safe():
    command = get_safe_command(request)
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/ip/safe2")
def safe2():
    command = get_safe_command(request)
    return execute_command(command)


@blueprint.route("/ip/vulnerable")
def vulnerable():
    source = get_vul_command(request)
    run = subprocess.run(source)  # sink. compromised input
    return str(run.returncode)
