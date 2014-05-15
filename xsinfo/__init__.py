from flask import Flask
import os
import sys


def configure_app(app, load_ek=False, conf_filename='conf.py',
                  secret_filename='app.key', ek_filename='encryption.key'):
    """
    http://flask.pocoo.org/snippets/104/
    """

    conf_filename = os.path.join(app.instance_path, conf_filename)
    secret_filename = os.path.join(app.instance_path, secret_filename)
    ek_filename = os.path.join(app.instance_path, ek_filename)

    try:
        app.config.from_pyfile(conf_filename)
    except IOError:
        print 'Error: No configuration file. Create it with:'
        if not os.path.isdir(os.path.dirname(conf_filename)):
            print 'mkdir -p {}'.format(os.path.dirname(conf_filename))
        print 'cp support/conf.py.example {}'.format(conf_filename)
        print '\nConfigure as needed.\n'
        sys.exit(1)

    try:
        app.config['SECRET_KEY'] = open(secret_filename, 'rb').read()
    except IOError:
        print 'Error: No secret key. Create it with:'
        print 'head -c 64 /dev/urandom > {}\n'.format(secret_filename)
        sys.exit(1)

    if load_ek:
        try:
            app.config['ENCRYPTION_KEY'] = open(ek_filename, 'rb').read()
        except IOError:
            print ('Error: No DB encryption key found. '
                   'Deloy before starting application.')
            sys.exit(1)

# init app
app = Flask(__name__, instance_relative_config=True)
configure_app(app, load_ek=True)

import xsinfo.views