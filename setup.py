from setuptools import setup

setup(
    name='Flask-Alcool',
    version='0.4',
    url='http://github.com/Kozea/flask-alcool',
    license='Beer License',
    author='Yohann Rebattu',
    author_email='yohann.rebattu@kozea.fr',
    description='Implement access control lists as decorators for flask.',
    long_description=__doc__,
    packages=['flask_alcool'],
    data_files=[('', ["LICENSE.txt"])],
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
