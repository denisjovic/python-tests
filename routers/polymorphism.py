import random

from flask import Blueprint, request
import subprocess

blueprint = Blueprint("polymorphism", __name__)


class A:
    def f(self, req):
        return "ls"


class B:
    def f(self, req):
        return req.args.get('key')


def get_vul_command(req):
    return req.args.get('key')


@blueprint.route("/pm/safe")
def safe():
    o = A()
    command = o.f(request)
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/pm/safe2")
def safe2():
    o = B()
    o = A()
    command = o.f(request)
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/pm/safe3")
def safe3():
    o = A()
    if False:
        o = B()
    command = o.f(request)
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/pm/safe4")
def safe4():
    x = [A(), B()]
    o = x[0]
    command = o.f(request)
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/pm/vulnerable")
def vulnerable():
    o = B()
    command = o.f(request)
    run = subprocess.run(command)  # sink. compromised input
    return str(run.returncode)


@blueprint.route("/pm/vulnerable2")
def vulnerable2():
    if random.random() > 0.5:
        o = B()
    else:
        o = A()
    command = o.f(request)
    run = subprocess.run(command)  # sink. compromised input
    return str(run.returncode)


@blueprint.route("/pm/vulnerable3")
def vulnerable3():
    x = [A(), B()]
    o = x[1]
    command = o.f(request)
    run = subprocess.run(command)  # sink. compromised input
    return str(run.returncode)
