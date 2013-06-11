from flask import Flask

#setup app
app = Flask(__name__)
app.config.from_object('config')

from pitchforksearch import views