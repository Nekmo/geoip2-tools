############
geoip2-tools
############


.. image:: https://img.shields.io/travis/Nekmo/geoip2-tools.svg?style=flat-square&maxAge=2592000
  :target: https://travis-ci.org/Nekmo/geoip2-tools
  :alt: Latest Travis CI build status

.. image:: https://img.shields.io/pypi/v/geoip2-tools.svg?style=flat-square
  :target: https://pypi.org/project/geoip2-tools/
  :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/geoip2-tools.svg?style=flat-square
  :target: https://pypi.org/project/geoip2-tools/
  :alt: Python versions

.. image:: https://img.shields.io/codeclimate/github/Nekmo/geoip2-tools.svg?style=flat-square
  :target: https://codeclimate.com/github/Nekmo/geoip2-tools
  :alt: Code Climate

.. image:: https://img.shields.io/codecov/c/github/Nekmo/geoip2-tools/master.svg?style=flat-square
  :target: https://codecov.io/github/Nekmo/geoip2-tools
  :alt: Test coverage

.. image:: https://img.shields.io/requires/github/Nekmo/geoip2-tools.svg?style=flat-square
     :target: https://requires.io/github/Nekmo/geoip2-tools/requirements/?branch=master
     :alt: Requirements Status


Automatic updates and administration of MaxMind GeoIP2 databases.


To install geoip2-tools, run this command in your terminal:

.. code-block:: console

    $ pip install geoip2-tools

This is the preferred method to install geoip2-tools, as it will always install the most recent stable release.


Usage
=====
To use this library you must first obtain a license from Maxmind. It is free for the geolite2 version of the database.

1. `Sign up for a Maxmind Geolite2 account <https://www.maxmind.com/en/geolite2/signup>`_
2. `Log in to your Maxmind account <https://www.maxmind.com/en/account/login>`_
3. In the menu on the left, navigate to ``Services > My License Key``.
4. Click ``Generate new license key``.
5. Save your license key in a secure site.

geoip2-tools downloads the latest version of the database and keeps it updated for you. By default every 7 days it is
downloaded from the Maxmind servers.

.. code-block:: python

    from geoip2_tools.manager import Geoip2DataBaseManager

    geoip2_manager = Geoip2DataBaseManager('<license key>')

    print(geoip2_manager['country'].reader.country('1.1.1.1').country.name)  # Australia

Geoip2-tools has aliases for the *city*, *country*, and *asn* Geolite2 databases. The country database is smaller than
city. The city database also contains the countries:

.. code-block:: python

    city = geoip2_manager['country'].reader.city('<ip address>')
    print(city.city.name)
    print(city.country.name)

To obtain the ASN you must use the asn database:

.. code-block:: python

    asn = geoip2_manager['country'].reader.asn('<ip address>')
    print(asn.autonomous_system_number)
    print(asn.autonomous_system_organization)
