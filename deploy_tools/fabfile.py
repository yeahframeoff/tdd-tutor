from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/yeahframeoff/tdd-tutor.git'

def deploy(folder):
    site_folder = '/sites/' + folder
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'venv', 'source', 'run'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git pull' % source_folder)
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = TRUE", "DEBUG = FALSE")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % site_name
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % key)
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    venv_folder = source_folder + '/../venv'
    if not exists(venv_folder + '/bin/pip3'):
        run('virtualenv --python=python3 %s' % venv_folder)
    run('%s/bin/pip3 install -r %s/requirements.pip' % (
        venv_folder, source_folder
    ))


def _update_static_files(source_folder):
    run('cd %s && ../venv/bin/python3 manage.py collectstatic --noinput' % source_folder)


def _update_database(source_folder):
    run('cd %s && ../venv/bin/python3 manage.py migrate --noinput' % source_folder)
