from flask import Blueprint, request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


blueprint = Blueprint("sqli", __name__)


def build_safe_query(id):
    stmt = text("SELECT * FROM users where id=:id")
    query = SQLAlchemy().session.query(User).from_statement(stmt).params(id=id)  # Compliant
    return query


def build_vul_query(id):
    stmt = text("SELECT * FROM users where id=%s" % id)  # Query is constructed based on user inputs
    query = SQLAlchemy().session.query(User).from_statement(stmt)  # Noncompliant
    return query


@blueprint.route("/sqli/safe")
def safe():
    id = request.args.get("id")
    stmt = text("SELECT * FROM users where id=:id")
    query = SQLAlchemy().session.query(User).from_statement(stmt).params(id=id)  # Compliant
    user = query.one()
    return "Hello %s" % user.username


@blueprint.route("/sqli/safe2")
def safe2():
    id = request.args.get("id")
    query = build_safe_query(id)
    user = query.one()
    return "Hello %s" % user.username


@blueprint.route("/sqli/vulnerable")
def vulnerable():
    id = request.args.get("id")
    stmt = text("SELECT * FROM users where id=%s" % id)  # Query is constructed based on user inputs
    query = SQLAlchemy().session.query(User).from_statement(stmt)  # Noncompliant
    user = query.one()
    return "Hello %s" % user.username


@blueprint.route("/sqli/vulnerable2")
def vulnerable2():
    id = request.args.get("id")
    query = build_vul_query(id)
    user = query.one()
    return "Hello %s" % user.username
