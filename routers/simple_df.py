from flask import Blueprint, request
import subprocess

blueprint = Blueprint("simple", __name__)


@blueprint.route("/simple/safe")
def safe():
    args = request.args
    run = subprocess.run("ls")  # sink. safe input
    return str(run.returncode)

@blueprint.route("/simple/safe2")
def safe2():
    args = request.args
    list1 = ["ls", "ll", "something else"]
    list2 = [args.get("key"), "ls"]
    run = subprocess.run(list1[0])  # sink. safe input
    return str(run.returncode)


@blueprint.route("/simple/vulnerable")
def vulnerable():
    command = request.args.get('key')
    run = subprocess.run(command)  # sink. compromised input
    return str(run.returncode)


@blueprint.route("/simple/vulnerable2")
def vulnerable2():
    list1 = ["ls"]
    command = request.args.get('key')
    list2 = [command, "ls"]
    run = subprocess.run(list2[0])  # sink. compromised input
    return str(run.returncode)
