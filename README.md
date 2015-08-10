#Flask-Alcool#

Flask-Alcool is a Flak extension to provide access control list like rights
management with decorators on routes. It also provide a jinja extension to
display only authorized links.

##Install##

```
pip install Flask-Alcool
```

##Examples##

###Protect routes###

```python
from flask.ext.alcool import alcool, allow_if
from myproject import app


@alcool
def drunk(**kwargs):
    return kwargs.get('drunk', False)


@alcool
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
```

In real life you may want to place all alcool decorated function in a
conditions.py file then do something like:

```python
import conditions as Is

@allow_if(Is.drunk | Is.major)
@app.route('/test/<int:age>/<bool:drunk>')
def protected_route(value, drunk):
    return "route is major or drunk or both"
```

Available alcool operators are:

-   ``a & b`` → ``a and b``
-   ``a | b`` → ``a or b``
-   ``a ^ b`` → ``a xor b``
-   ``~ a`` → ``not a``


###Display links only for authorized routes###

Use this snippet to configure Jinja2:

```python
from flask.ext.alcool import Alcool
alcool = Alcool(app)
```

Then, in templates you can use the new {% auth %} block:

```html+jinja
{% auth 'drive', {'drunk': false} %}
  This text will be displayed
{% endauth %}
{% auth 'drive', {'drunk': true} %}
  This text will not be displayed
{% endauth %}
```
