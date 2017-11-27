"""
Jinja2 auth conditional url display extensions.

"""

from jinja2 import nodes
from jinja2.ext import Extension

from .alcool import if_auth_url_for


class UrlIfAuthExtension(Extension):
    """Jinja block which check auth on a link to display it or not."""
    tags = set(['auth'])

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        url = parser.parse_expression(with_condexpr=False)
        url_var = nodes.Name('checked_url', 'store')
        args = None
        if parser.stream.current.type != 'block_end':
            parser.stream.expect('comma')
            args = parser.parse_expression(with_condexpr=False)

        fun_var = parser.free_identifier()
        body = parser.parse_statements(('name:endauth', 'name:else'))
        token = next(parser.stream)
        if token.test('name:else'):
            else_ = parser.parse_statements(
                ('name:endauth', ), drop_needle=True)
        else:
            else_ = None
        url_fun_tuple = nodes.Tuple([url_var, fun_var], 'store')
        # The url goes in the dyn_args (its not visited otherwise).
        # To be in the dyn_args, it must be wrapped in a Tuple.
        assignment = nodes.Assign(url_fun_tuple,
                                  self.call_method(
                                      'template_if_auth_url_for',
                                      dyn_args=nodes.Tuple([url], 'load'),
                                      dyn_kwargs=args)).set_lineno(lineno)

        returned_ast = [assignment]
        if_node = nodes.If()
        if_node.test = nodes.Name('checked_url', 'load')
        if_node.body = body
        if_node.else_ = else_
        if_node.elif_ = []
        returned_ast.append(if_node.set_lineno(lineno))
        return returned_ast

    def template_if_auth_url_for(self, url, **kwargs):
        """Make a convenience method here to use call_method, and not
        an import name"""
        return if_auth_url_for(url, **kwargs)
