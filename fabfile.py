#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os
# noinspection PyPackageRequirements
from fabric import task


@task
def vagrant(c):
    """Vagrant environment"""
    c.env.environment = 'local'
    c.env.user = 'vagrant'
    c.env.hosts = ['127.0.0.1:2222']
    result = c.local('vagrant ssh-config | grep IdentityFile', capture=True)
    c.env.key_filename = result.split()[1]


# noinspection PyUnusedLocal
@task
def clean(c):
    """Remove temporary files."""
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.pyc') or name.endswith('~'):
                os.remove(os.path.join(root, name))


@task
def devserver(c, port=8000, logging='error'):
    """Start the server in development mode."""
    c.run('python run.py --port=%s --logging=%s' % (port, logging))
