from flask import Flask
import os
import sys


def configure_app(app, load_ek=False, conf_file='app.conf',
                  secret_file='app.key', ek_file='encryption.key'):
    """
    http://flask.pocoo.org/snippets/104/
    """

    conf_file = os.path.join(app.instance_path, conf_file)
    secret_file = os.path.join(app.instance_path, secret_file)
    ek_file = os.path.join(app.instance_path, ek_file)

    try:
        app.config.from_pyfile(conf_file)
    except IOError:
        print 'Error: No configuration file. Create it with:'
        if not os.path.isdir(os.path.dirname(conf_file)):
            print 'mkdir -p {}'.format(os.path.dirname(conf_file))
        print 'cp support/conf.py.example {}'.format(conf_file)
        print '\nConfigure as needed.\n'
        sys.exit(1)

    try:
        app.config['SECRET_KEY'] = open(secret_file, 'rb').read()
    except IOError:
        print 'Error: No secret key. Create it with:'
        print 'head -c 32 /dev/urandom > {}\n'.format(secret_file)
        sys.exit(1)

    if load_ek:
        try:
            app.config['ENCRYPTION_KEY'] = open(ek_file, 'rb').read()
        except IOError:
            print ('Error: No DB encryption key found. '
                   'Deloy before starting application.')
            sys.exit(1)


def configure_logging(app, log_file='app.log', log_size=1048576, log_backups=5):
    if app.debug:
        import logging
        from logging import Formatter
        from logging.handlers import RotatingFileHandler

        log_file = os.path.join(app.instance_path, log_file)

        file_handler = RotatingFileHandler(
            filename=log_file, maxBytes=log_size, backupCount=log_backups
        )
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))

        app.logger.addHandler(file_handler)

# init app
app = Flask(__name__.split('.')[0], instance_relative_config=True)
configure_app(app, load_ek=True)
configure_logging(app)
import xsinfo.views