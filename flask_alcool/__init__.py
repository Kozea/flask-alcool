"""
flask.ext.alcool
~~~~~~~~~~~~~~~~

Implement access control lists as decorators for flask.

:copyright: (c) 2015 by Florient Mounier, Yohann Rebattu.
:license: BeerLicense, see LICENSE for more details.

"""

from .alcool import allow_if, alcool


class Alcool:
    def __init__(self, app=None, configure_jinja=True):
        self._configure_jinja = configure_jinja
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.alcool_instance = self

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['alcool'] = self

        if self._configure_jinja:
            from .url_if_auth import UrlIfAuthExtension
            app.jinja_env.add_extension(UrlIfAuthExtension)
