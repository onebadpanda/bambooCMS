__author__ = 'One Bad Panda'
from obp import app
from obp.views import admin, standard


app.run(host='0.0.0.0',debug=True)