# googleoauth2django

oauth2client is deprecated and there seems to be no path forward for poor souls who used the contrib/django_util code from it.

So I converted django_util to support Django >=2, Python 3.6, and google-auth-oauthlib.
See: https://github.com/googleapis/google-auth-library-python/issues/181


## Notes
AFAIK, all unit tests are passing, 100% coverage was maintained from oauth2client, and the docs are appropriately changed.

The pipenv files (Pipfile, Pipfile.lock) are in VCS for convenience; the required libs are explicitly in setup.py.

I had to make some arbitrary decisions:
 * Credentials go into the CredentialsField ORM using jsonpickle.
 * Rather than storing the "Flow" object into request.session, I store a "flow_settings" that can be used to construct the flow, as the Flow object isn't serializable.

I left the old oauth2client files within `deprecated/`, and attempted to leave the git history sensible so it's clear what files went where.

## Development
Install editable: `pip install -e .[dev]`

Build docs: `tox -e docs`

Run tests: `python manage.py test`

Run coverage test with tox: `tox -e cover`

Run flake8 with tox: `tox -e flake8`

I added a django "manage.py" that can be run with `python manage.py runserver`.
