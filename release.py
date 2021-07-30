import os
import subprocess
import sys


def call(cmd, capture_output=False):
    if isinstance(cmd, str):
        cmd = cmd.split()  # no user-input will come here. This is safe.
    print(cmd)
    result = subprocess.run(cmd, capture_output=capture_output)
    if result.returncode == 0:
        print('    ok')
        return result
    print(result.stdout)
    print(result.stderr)
    print(f'failed. {result.returncode}')
    sys.exit()


def check_git_is_clean():
    result = call(['git', 'status', '--porcelain'], capture_output=True)
    if result.stdout:
        print(result.stdout.decode())
        print('Git not clean. Commit first')
        sys.exit(1)


def check_tests_and_coverage():
    call(
        'pytest --cov-report=html --no-cov-on-fail --cov --cov-fail-under=75 --create-db --exitfirst'.split())


def main():
    os.chdir(os.path.join(os.getenv('VIRTUAL_ENV'), 'src/django-trace-cockpit'))
    check_git_is_clean()
    check_tests_and_coverage()
    call(['git', 'push'])
    call('python setup.py sdist')
    call('pip install twine')
    call('twine upload dist/*')


if __name__ == '__main__':
    main()
