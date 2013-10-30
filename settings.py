#!/usr/bin/env python
#fileencoding=utf-8

import logging
from tornado.options import define

def define_app_options():
    define('debug', default=True)
    define('log_level', default=logging.INFO)
    define('cookie_secret', default='<to be added.>')

    define('port', default=9888)

    try:
        from local_settings import setup
        setup()
    except ImportError:
        pass
