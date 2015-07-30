#Flask-Acl#

Flask acl is a Flak extension to provide access control list like rights
management with decorators on routes. It also provide a jinja extension
to display only authorized links.

##Exemple:##

'''
from flask.ext.acl import acl, allow_if
from myproject import app


@acl
def drunk(**kwargs):
    return kwargs.get('drunk', False)


@acl
def major(**kwargs):
    value = kwargs.get('value', 0)
    return True if value > 18 else False


@allow_if(drunk | major)
@app.route('/test/<int:age>/<bool:drunk>')
def protected_route(value, drunk):
    return "route is major or drunk or both"


@allow_if(~drunk)
@app.route('/drive/<bool:drunk>')
def drive(drunk):
    return "route is sober : drive safely"


@allow_if(major & ~drunk)
@app.route('/welcome/<bool:drunk>/<int:value>')
def welcome_home(drunk, value):
    return "route is major and sober"
'''

In real life you may want to place all acl decorated function in a
conditions.py file then do something like:

'''
import conditions as Is


@allow_if(Is.drunk | Is.major)
@app.route('/test/<int:age>/<bool:drunk>')
def protected_route(value, drunk):
    return "route is major or drunk or both"
'''

availables acl operators are:

 -   ``a & b`` -> ``a and b``
 -   ``a | b`` -> a or  b``
 -   ``a ^ b`` -> a xor b``
 -   ``~ a`` -> not a``
