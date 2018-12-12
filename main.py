# run.py

import os

# local imports
from app import create_app
from werkzeug.serving import make_ssl_devcert

config_name = "development"#os.getenv('FLASK_CONFIG')

app = create_app(config_name)

if __name__ == "__main__":

    #make_ssl_devcert('./ssl', host='0.0.0.0')
    #app.run(host='0.0.0.0', port=80, ssl_context=('./ssl.crt', './ssl.key'), threaded = True)
    #make_ssl_devcert('./ssl', host='0.0.0.0')
    app.run(host='0.0.0.0', port=8081)
