from setuptools import setup

setup(
    name='Flask-Alcool',
    version='0.2',
    url='http://github.com/Kozea/flask-acl',
    license='Beer License',
    author='Yohann Rebattu',
    author_email='yohann.rebattu@kozea.fr',
    description='Add acl like support on flask routes',
    long_description=__doc__,
    packages=['flask_acl'],
    zip_safe=False,
    install_requires=[
        'Flask',
        'Jinja2>=2.5'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
