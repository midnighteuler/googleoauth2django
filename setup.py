"""Setup script for googleoauth2django."""
from setuptools import find_packages
from setuptools import setup

long_desc = """
googleoauth2django is oauth2client.contrib.django_util redone to instead use 
google-auth-oauthlib and supports django 2, as oauth2client was deprecated.
"""

dev_deps = [
    'pytest',
    'mock>=2.0.0',
    'ipdb>=0.11',
    'django-extensions'
]
extras = {
    'dev': dev_deps
}
setup(
    name='googleoauth2django',
    version='0.0.1',
    description='oauth2client.contrib.django_util sans oauth2client',
    long_description=long_desc,
    author='Michael Souza',
    author_email='mike@michaelsouza.com',
    url='http://github.com/midnighteuler/googleoauth2django/',
    install_requires=[
        'django>=2.1.5',
        'google-auth-oauthlib>=0.2.0',
        'google-auth>=1.6.2',
        'requests-oauthlib>=1.0.0',
        'oauthlib>=2.1.0',
        'jsonpickle>=1.0',
        'six'
    ],
    tests_require=dev_deps,
    extras_require=extras,
    packages=find_packages(exclude=('tests*', 'deprecated*')),
    license='Apache 2.0',
    keywords='google oauth 2.0 django',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
