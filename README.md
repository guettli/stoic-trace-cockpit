# stoic-trace-cockpit

# Why "stoic-trace-cockpit"?

I develop Django applications since 2009. Nevertheless sometimes I don't understand what is going on.
I would like to see what the Python interpreter is doing while processing my http request.

With "trace" I mean an output similar to `set -x` in the bash shell. Every line should be visible,
with a flexible include/exclude filter.

With "cockpit" I mean a web-interface. You can enable and disable the tracing without touching source code.

The Stoic Trace Cockpit is meant to be useful during development and live on production.

# Install

```
python3 -m venv stoic-trace-cockpit-env
cd stoic-trace-cockpit-env/
. bin/activate
pip install -U pip wheel
pip install -e git+ssh://git@github.com/guettli/stoic-trace-cockpit.git#egg=stoic-trace-cockpit
cp src/stoic-trace-cockpit/.env.example src/stoic-trace-cockpit/.env
echo '. $VIRTUAL_ENV/src/stoic-trace-cockpit/.env' >> bin/activate
echo 'export $(cut -d= -f1 $VIRTUAL_ENV/src/stoic-trace-cockpit/.env)' >> bin/activate

. bin/activate

# You need to have PostgreSQL installed
# Create user "stoic-trace-cockpit" with password "stoic-trace-cockpit":
sudo runuser -u postgres -- createuser -s -P stoic-trace-cockpit

createdb $PGDATABASE
manage.py migrate
```

The migration create a user "anonymous" (for not authorized users) and "admin" (with password "admin").

# Naming convention

See: https://github.com/guettli/django-htmx-fun

# Guidelines

See: https://github.com/guettli/programming-guidelines

