# stoic-trace-cockpit

# Why "stoic-trace-cockpit"?

I develop Django applications since 2009. Nevertheless sometimes I don't understand what is going on.
I would like to see what the Python interpreter is doing while processing my http request.

With "trace" I mean an output similar to `set -x` in the bash shell. Every line should be visible,
with a flexible include/exclude filter.

With "cockpit" I mean a web-interface. You can enable and disable the tracing without touching source code.

The Stoic Trace Cockpit is meant to be useful during development and live on production.

# Status: Alpha

Up to now this project is just starting.

# Models

There are two database models which are both part of the Django-Admin.

## TraceConfig

With a TraceConfig you can configure which requests and which modules you want to trace.

## TraceLog

If a http request matches a TraceConfig, then it gets traced by the middleware and the result gets
stored in a TraceLog. 

In the TraceLog you see which Python source code lines where executed during processing the request.

# Install

If you have a Django project, and you want use it inside your existing project:

```
pip install stoic-trace-cockpit
```

If you want use a new virtual environment, then this installs the Stoic Trace Cockpit and
a small test project:

```
python3 -m venv stc-env
cd stc-env/
. bin/activate
pip install -U pip wheel
pip install -e git+ssh://git@github.com/guettli/stoic-trace-cockpit.git#egg=stoic-trace-cockpit
cp src/stoic-trace-cockpit/.env.example src/stoic-trace-cockpit/.env
echo '. $VIRTUAL_ENV/src/stoic-trace-cockpit/.env' >> bin/activate
echo 'export $(cut -d= -f1 $VIRTUAL_ENV/src/stoic-trace-cockpit/.env)' >> bin/activate

. bin/activate

python setup-development-environment.py

# You need to have PostgreSQL installed
# Create user "stoic-trace-cockpit" with password "stoic-trace-cockpit":
sudo runuser -u postgres -- createuser -s -P stoic-trace-cockpit

createdb $PGDATABASE
manage.py migrate
```

The migration create a user "anonymous" (for not authorized users) and "admin" (with password "admin").

# Configure

If you use the dummy-project, then you can skip this.

If you use Stoic Trace Cockpit in your existing Django project, then add this to settings.INSTALLED_APPS:

```
    'trace_cockpit',
    'ordered_model',
```

Add this to `MIDDLEWARE`:

```
    'trace_cockpit.middleware.TraceMiddleware',
```

A good place for it is below "AuthenticationMiddleware", because you migh twant to trace http-request for a particular user. This is only possible if `request.user` already exists.


# Naming convention

See: https://github.com/guettli/django-htmx-fun

# Guidelines

See: https://github.com/guettli/programming-guidelines

