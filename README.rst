===============================
block_trade_desk
===============================

.. image:: https://badge.fury.io/py/block_trade_desk.png
    :target: http://badge.fury.io/py/block_trade_desk

.. image:: https://pypip.in/d/block_trade_desk/badge.png
    :target: https://crate.io/packages/block_trade_desk?version=latest


block_trade_desk website

* Free software: BSD license

Requirements
------------

* Django 1.10+
* Python 2.7
* Django CMS 3.4+

.. _django-cms: https://github.com/divio/django-cms

Installation
----------------------------

#. Clone the git repository.
#. Create a production.py file in block_trade_desk/block_trade_desk/block_trade_desk/settings by copying what's in the example_production.py
    * Fill database details in the file you just created
    * Add the site admins in the ADMINS variable
    * Add server host in ALLOWED_HOSTS

#. Install all third party packages by running::

    $ pip install -r requirements/development.txt

#. Apply migrations::

    $ python manage.py migrate

