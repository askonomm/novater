from flask import Flask
from routes.api import api
from routes.site import site

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(site)
