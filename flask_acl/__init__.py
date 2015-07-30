"""
    flask.ext.acl
    ~~~~~~~~~~~~~

    Implements access control list like decorators for flask.

    :copyright: (c) 2015 by Florient Mounier, Yohann Rebattu.
    :license: BeerLicense, see LICENSE for more details.
"""
from .acl import allow_if, acl


class Acl():
    def __init__(self, app=None, configure_jinja=True):
        self._configure_jinja = configure_jinja
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.acl_instance = self

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['acl'] = self

        if self._configure_jinja:
            from .url_if_auth import UrlIfAuthExtension
            app.jinja_env.add_extension(UrlIfAuthExtension)
