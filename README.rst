======
opslab
======

opslab is a simple Django app to manage svn server. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Get opslab::

    git clone https://github.com/ops-lab/opslab.git

2. Change configuration::

    Update Ldap configuration:
        opslab.user.management

    Replace the following file contents with valid file contents::

            # auth file for svn
            opslab/opslab/common/statics/dav_svn.authz
            # manager, url
            opslab/opslab/common/statics/owner_url_map
            # module, preurl
            opslab/opslab/common/statics/module_preurl_map

3. Create Database in MySQL Database::

    CREATE DATABASE opslab DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

4. Install opslab as a library for Python::

    make install

5. Modify opslab.setting::

    Change default database host "127.0.0.1" to wanted database host

6. Run `python manage.py makemigrations` to create the app migrations, and run `python manage.py migrate` to create the user models::

    python manage.py makemigrations user
    python manage.py migrate user

    python manage.py makemigrations autosolution
    python manage.py migrate autosolution

    python manage.py makemigrations
    python manage.py migrate

7. Prepare frontend static file(directory is dist/)::

    mkdir -p $python_site_packages/opslab/frontend/
    cp -rf dist/* $python_site_packages/opslab/frontend/

8. Run opslab::

    python3.7 manage.py runserver 0.0.0.0:8000

9. Start use or develop opslab.

Quick Develop
-------------

1. Add "user" to your PLUGIN_APPS setting like this::

    PLUGIN_APPS = [
        ...
        'user',
    ]

2. Include the user URLconf in your project urls.py like this::

    path('user/', include('user.urls')),

3. Run `python manage.py makemigrations user` to create the user migrations.

4. Run `python manage.py migrate user` to create the user models.

5. Add frontend static file to opslab/frontend. And start the development 
   server that run `python manage.py runserver 0.0.0.0:8000`.

6. Visit http://127.0.0.1:8000/ to participate in the user.
