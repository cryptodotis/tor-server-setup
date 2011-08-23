"""
To setup a new server:

-- Run this script with
    - fab create_tor_user
	- fab tor_host setup_server
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

def setup_ssh_keys():
    with cd('/home/%s/' % FAB_USER):
        run('mkdir .ssh/')
    with cd('/home/%s/.ssh/' % FAB_USER):
        run('ssh-keygen -b 4096 -t rsa -f /home/%s/.ssh/id_rsa -P ""' %
FAB_USER)

def add_to_sudoers():
   run('echo "%s    ALL=(ALL) ALL" >> /etc/sudoers' % FAB_USER)

def create_tor_user():
    ubuntu_update()
    add_tor_user()
    setup_ssh_keys()
    add_to_sudoers()

# Install Git

def install_git():
	sudo('apt-get -y install git-core')

def add_github_keys():
    with cd('/home/%s/.ssh/' % FAB_USER):
        sudo('ssh-keyscan github.com >> authorized_keys')
        sudo('ssh-keyscan github.com >> known_hosts')

def clone_tor_setup_repo():
    with cd('/home/%s/' % FAB_USER):
        sudo('git clone git://github.com/cryptodotis/tor-server-setup.git')

def setup_git():
    install_git()
    add_github_keys()
    clone_tor_setup_repo()

def add_tor_gpg_key():
	sudo('apt-key adv --keyserver keys.gnupg.net --recv 886DDD89')

def append_tor_repos_to_sources():
    sudo('echo "deb http://deb.torproject.org/torproject.org maverick main" >> /etc/apt/sources.list')
    sudo('echo "deb-src http://deb.torproject.org/torproject.org maverick main" >> /etc/apt/sources.list')


def apt_get_update():
	sudo('apt-get update')

def apt_get_tor():
	sudo('apt-get -y install tor tor-geoipdb')

def copy_tor_config():
	with cd('~/tor-relay-setup/files/'):
		sudo('cp torrc /etc/tor/torrc')

def restart_tor():
    sudo('/etc/init.d/tor restart')

def install_tor():
    add_tor_gpg_key()
    append_tor_repos_to_sources()
    apt_get_update()
    apt_get_tor()
    copy_tor_config()
    restart_tor()

# Setting up torproject.org mirror

def apt_get_rsync():
    sudo('apt-get -y install rsync')

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


def setup_mirror():
    apt_get_rsync()
    setup_nginx()


def setup_server():
    setup_git()
    install_tor()
    setup_mirror()
