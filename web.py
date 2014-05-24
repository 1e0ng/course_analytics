#!/usr/bin/env python
#fileencoding=utf-8
import os
import time
import signal
import logging

from tornado.httpserver import HTTPServer
from tornado.web import StaticFileHandler, Application
from tornado.ioloop import IOLoop
from tornado.options import options, parse_command_line
from jinja2 import Environment, ChoiceLoader, FileSystemLoader

import settings

class JinjaTemplate(object):
    def __init__(self,  template):
        self.template = template

    def generate(self,  **kwargs):
        return self.template.render(**kwargs)

class JinjaLoader(object):
    def __init__(self,  **kwargs):
        super(JinjaLoader,  self).__init__(**kwargs)

        path = os.path.abspath(os.path.join(__file__, '../templates'))

        loader = ChoiceLoader([
            FileSystemLoader(path),
            ])

        self.env = Environment(loader=loader)

    def load(self,  name,  parent_path=None):
        return JinjaTemplate(self.env.get_template(name))

    def reset(self):
        self.env.cache.clear()

def install_tornado_shutdown_handler(ioloop, server):
    # see https://gist.github.com/mywaiting/4643396 for more detail

    def _sig_handler(sig, frame):
        logging.info("Signal %s received. Preparing to stop server.", sig)
        ioloop.add_callback(shutdown)

    def shutdown():
        logging.info("Stopping http server...")
        server.stop()

        MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3
        logging.info("Will shutdown in %s seconds",
                    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

        def stop_loop():
            now = time.time()
            if now < deadline and (ioloop._callbacks or ioloop._timeouts):
                ioloop.add_timeout(now + 1, stop_loop)
                logging.debug("Waiting for callbacks and timeouts in IOLoop...")
            else:
                ioloop.stop()
                logging.info("Server is shutdown")

        stop_loop()

    signal.signal(signal.SIGTERM, _sig_handler)
    signal.signal(signal.SIGINT, _sig_handler)

class App(Application):
    def __init__(self, options):
        app_settings = {
            'template_loader': JinjaLoader(),
            'debug': options.debug,
            'cookie_secret': options.cookie_secret,
        }
        self.name = 'Enjoy Study'
        self.db = None

        the_routes = [
                (r'/', 'controller.MainHandler'),
                (r'/static/(.*)', StaticFileHandler, {"path": "static"}),
            ]
        super(App, self).__init__(the_routes, **app_settings)

def main():
    settings.define_app_options()
    parse_command_line(final=True)

    logging.info('Runing at port %s in %s mode' % (options.port, 'debug' if options.debug else 'production'))

    app = App(options)
    server = HTTPServer(app, xheaders=True)
    server.listen(options.port)

    install_tornado_shutdown_handler(IOLoop.instance(), server)
    logging.info('Good to go!')

    IOLoop.instance().start()
    logging.info('Exiting...waiting for background jobs done...')
    logging.info('Done. Bye.')

if __name__ == "__main__":
    import sys
    sys.exit(main())
