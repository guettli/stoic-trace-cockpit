from subprocess import run

development_requirements=[
    'pytest-django',
    'python-dotenv',
    'psycopg2-binary',
    'whitenoise',
    'pre-commit',
    'django-check-html-middleware',
    'pytest-cov',
]
cmd = 'pip install {}'.format(' '.join(development_requirements))
run(cmd.split())