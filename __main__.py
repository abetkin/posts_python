from flask import Flask
from flask.ext.cors import CORS
from flask_graphql import GraphQL
from schema import schema

app = Flask(__name__, static_url_path='/static/')
app.debug = True
graphql = GraphQL(app, schema=schema)

CORS(app)


app.run()

