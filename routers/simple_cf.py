from flask import Blueprint, request
import subprocess
from random import random

blueprint = Blueprint("simple_cf", __name__)


@blueprint.route("/simple_cf/safe")
def safe():
    command = "ls"
    if False:
        command = request.args.get('key')  # tainted
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/simple_cf/safe2")
def safe2():
    command = "ls"
    while False:
        command = request.args.get('key')  # tainted
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/simple_cf/safe3")
def safe3():
    command = request.args.get('key')  # tainted
    command = "ls"  # safe
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/simple_cf/safe4")
def safe4():
    command = request.args.get('key')  # tainted
    if True:
        command = "ls"  # safe
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/simple_cf/safe5")
def safe5():
    command = request.args.get('key')  # tainted
    try:
        random()
        command = "ls"  # safe
    except:
        command = "pwd"  # safe
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/simple_cf/vulnerable")
def vulnerable():
    command = "constant"
    if random() > 0.5:
        command = request.args.get('key')
    run = subprocess.run(command)  # sink. compromised input
    return str(run.returncode)


@blueprint.route("/simple_cf/vulnerable2")
def vulnerable2():
    command = "constant"
    while random() > 0.5:
        command = request.args.get('key')
    run = subprocess.run(command)  # sink. compromised input
    return str(run.returncode)


@blueprint.route("/simple_cf/vulnerable3")
def vulnerable3():
    try:
        if random() > 0.5:
            raise Exception()
        command = "constant"
    except:
        command = request.args.get('key')
    run = subprocess.run(command)  # sink. compromised input
    return str(run.returncode)
