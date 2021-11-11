from flask import Flask
from routers import simple_df, simple_cf, interprocedural, mro, cbs, fields, polymorphism, sqli

app = Flask(__name__)
routers = [simple_df, simple_cf, interprocedural, mro, cbs, fields, polymorphism, sqli]
for r in routers:
    app.register_blueprint(r.blueprint)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
