
Fixtures
========

You can populate the database with some *fake* data.

* Create a database ``createdb kumotest``
* Type ``psql kumo_test``
* Execute the ``fixtures`` SQL file

::

   \i fixtures.sql


Get and Clean the Data
======================

Download the ``Airbase_v8`` zip file with the Python script ``get.py`` and
extract the data (in a CSV file).

Then, launch the script ``raw_to_csv.py`` to extract some data from the raw
Airbase CSV file. This create a ``airbase.csv`` file with some data that Kumo
use.

Kept data:

* ``code``: unique code station name
* ``country``: the country
* ``height``: the height (in meter)
* ``lat``: latitude
* ``lon``: longitude
* ``name``: station name
* ``type``: station type (background, traffic, industrial)


Data in the Database
====================

Create the database, ``kumo`` for instance, and then:

::

   \i airbase.sql

in the ``psql`` prompt.

It creates the table ``stations`` and carries out a ``COPY`` from the *cleaned*
Airbase CSV file.

Simple queries:

.. code-block: sql

   SELECT name,code,type FROM stations LIMIT 20;

.. code-block: sql

   SELECT COUNT(name),type FROM station GROUP BY type;
