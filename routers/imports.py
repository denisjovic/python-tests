# import random
#
# from flask import Blueprint, request
# import subprocess
#
# blueprint = Blueprint("mro", __name__)
#
#
# @blueprint.route("/mro/safe")
# def safe():
#     o = C()
#     command = o.f(request)
#     run = subprocess.run(command)  # sink. safe input
#     return str(run.returncode)
#
#
# @blueprint.route("/mro/vulnerable")
# def vulnerable():
#     o = B()
#     command = o.f(request)
#     run = subprocess.run(command)  # sink. compromised input
#     return str(run.returncode)
