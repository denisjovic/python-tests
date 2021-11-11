from flask import Blueprint, request
import subprocess

blueprint = Blueprint("field", __name__)


class A:
    def __init__(self, f):
        self.f = f

    def get_f(self):
        return self.f

    def set_f(self, f):
        self.f = f


class B:
    pass


class C:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_a(self):
        return self.a

    def get_b(self):
        return self.b


@blueprint.route("/field/safe")
def safe():
    a1 = A(request.args.get('key'))
    a2 = A("ls")
    run = subprocess.run(a2.f)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/field/safe2")
def safe2():
    a1 = A(request.args.get('key'))
    a1.f = "ls"
    run = subprocess.run(a1.get_f())  # sink. safe input
    return str(run.returncode)


@blueprint.route("/field/safe3")
def safe3():
    a1 = A(request.args.get('key'))
    a1.set_f("ls")
    run = subprocess.run(a1.get_f())  # sink. safe input
    return str(run.returncode)


@blueprint.route("/field/safe4")
def safe4():
    c = C("ls", request.args.get('key'))
    run = subprocess.run(c.a)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/field/safe5")
def safe5():
    c = C("ls", C(request.args.get('key'), "ls"))
    a = A(c)
    cmd = a.get_f().get_a()
    run = subprocess.run(cmd)  # sink. safe input
    return str(run.returncode)


@blueprint.route("/field/vulnerable")
def vulnerable():
    a1 = A(request.args.get('key'))
    a2 = A("ls")
    run = subprocess.run(a1.f)
    return str(run.returncode)


@blueprint.route("/field/vulnerable2")
def vulnerable2():
    b = B()
    b.x = request.args.get('key')
    run = subprocess.run(b.x)
    return str(run.returncode)


@blueprint.route("/field/vulnerable3")
def vulnerable3():
    c = C("ls", request.args.get('key'))
    run = subprocess.run(c.b)
    return str(run.returncode)


@blueprint.route("/field/vulnerable4")
def vulnerable4():
    a = A("ls")
    c = C("ls", request.args.get('key'))
    a.set_f(c.b)
    run = subprocess.run(a.get_f())
    return str(run.returncode)


@blueprint.route("/field/vulnerable5")
def vulnerable5():
    c = C(C(request.args.get('key'), "ls"), "ls")
    a = A(c)
    cmd = a.get_f().get_a().get_a()
    run = subprocess.run(cmd)
    return str(run.returncode)
