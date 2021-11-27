from flask import Flask

app = Flask(__name__)
app.secret_key = 'cf89bbdb47fedba7531ac685316667bf'

import application.plot_feature_importances
