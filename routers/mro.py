import random

from flask import Blueprint, request
import subprocess

blueprint = Blueprint("mro", __name__)


class A:
    def f(self, req):
        return "ls"


class B:
    def f(self, req):
        return req.args.get('key')


class C(A, B):
    pass


class D(B, A):
    pass


class E(C, B):
    pass


def get_vul_command(req):
    return req.args.get('key')


@blueprint.route("/mro/safe")
def safe():
    o = C()
    command = o.f(request)
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/mro/safe2")
def safe2():
    o = E()
    command = o.f(request)
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/mro/safe3")
def safe3():
    o = C()
    if False:
        o = B()
    command = o.f(request)
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/mro/safe4")
def safe4():
    x = [A(), B()]
    o = x[0]
    command = o.f(request)
    run = subprocess.run(command)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/mro/vulnerable")
def vulnerable():
    o = B()
    command = o.f(request)
    run = subprocess.run(command)  # sink. compromised input
    return str(run.returncode)


@blueprint.route("/mro/vulnerable2")
def vulnerable2():
    if random.random() > 0.5:
        o = B()
    else:
        o = A()
    command = o.f(request)
    run = subprocess.run(command)  # sink. compromised input
    return str(run.returncode)


@blueprint.route("/mro/vulnerable3")
def vulnerable3():
    o = D()
    command = o.f(request)
    run = subprocess.run(command)  # sink. compromised input
    return str(run.returncode)
