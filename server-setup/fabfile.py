"""
To setup a new server:

-- Run this script with
	- fab set_host set_user_server setup_server
"""
import crypt, getpass, pwd

from fabric.api import env, sudo, local, run, require
from fabric.context_managers import cd

from settings import HOST, ROOT_USER, ROOT_PASS, FAB_USER, FAB_PASS

env.hosts = ['%s@%s' % (ROOT_USER, HOST)]

env.passwords = {'%s@%s' % (ROOT_USER, HOST): ROOT_PASS, 
                 '%s@%s' % (FAB_USER, HOST): FAB_PASS}

def root_host():
    env.hosts = ['%s@%s' % (ROOT_USER, HOST)]

def tor_host():
    env.hosts = ['%s@%s' % (FAB_USER, HOST)]

def ubuntu_update():
    run('apt-get update')

def add_tor_user():
    run('useradd -s /bin/bash -m %s' % FAB_USER)
    run('echo -e "%s\\n%s" | passwd %s' % (FAB_PASS, FAB_PASS, FAB_USER))

# Install Git

def install_git():
	sudo('apt-get -y install git-core')

def add_tor_gpg_key():
	run('apt-key adv --keyserver keys.gnupg.net --recv 886DDD89')

def append_tor_repos_to_sources():
    run('echo "deb http://deb.torproject.org/torproject.org maverick main" >> /etc/apt/sources.list')
    run('echo "deb-src http://deb.torproject.org/torproject.org maverick main" >> /etc/apt/sources.list')


def apt_get_update():
	run('apt-get update')

def apt_get_tor():
	run('apt-get -y install tor tor-geoipdb')

def install_tor():
    add_tor_gpg_key()
    append_tor_repos_to_sources()
    apt_get_update()
    apt_get_tor()

# Setting up torproject.org mirror

def apt_get_rsync():
    run('apt-get -y install rsync')

# Nginx
def install_nginx():
	sudo('apt-get -y install nginx')

def copy_nginx_config():
	with cd('~/tor-relay-setup/files/'):
		sudo('cp nginx.conf /etc/nginx/nginx.conf')

def restart_nginx():
	sudo('/etc/init.d/nginx restart')

def setup_nginx():
	install_nginx()
	copy_nginx_config()
	restart_nginx()


