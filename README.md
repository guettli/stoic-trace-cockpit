# django-trace-cockpit

# Install

```
python3 -m venv django-trace-cockpit-env
cd django-trace-cockpit-env/
. bin/activate
pip install -U pip wheel
pip install -e git+ssh://git@github.com/guettli/django-trace-cockpit.git#egg=django-trace-cockpit
cp src/django-trace-cockpit/.env.example src/django-trace-cockpit/.env
echo '. $VIRTUAL_ENV/src/django-trace-cockpit/.env' >> bin/activate
echo 'export $(cut -d= -f1 $VIRTUAL_ENV/src/django-trace-cockpit/.env)' >> bin/activate

. bin/activate

# You need to have PostgreSQL installed
# Create user "django-trace-cockpit" with password "django-trace-cockpit":
sudo runuser -u postgres -- createuser -s -P django-trace-cockpit

createdb $PGDATABASE
manage.py migrate
```

The migration create a user "anonymous" (for not authorized users) and "admin" (with password "admin").

# Naming convention

See: https://github.com/guettli/django-htmx-fun

# Guidelines

See: https://github.com/guettli/programming-guidelines

