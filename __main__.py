from flask import Flask
from flask_graphql import GraphQL
from schema import Schema

app = Flask(__name__, static_url_path='/static/')
app.debug = True
graphql = GraphQL(app, schema=Schema)


app.run()

