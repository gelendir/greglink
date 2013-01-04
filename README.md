Greglink
========

Simple test case management webapp, loosely inspired by [Jekyll](https://github.com/mojombo/jekyll).
Greglink takes a "test directory", runs all the files through markdown and shows the tests that need to be executed
on the web site.

Setup
=====

get the code:
    git clone git://github.com/gelendir/greglink

install the python dependencies:
    virtualenv2 env
    source env/bin/activate
    pip install -r requirements.txt

create config file:
    cp greglink/default_config.py localconfig.py

edit config file:
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/greglink.db'
    TEST_ROOT = '/tmp/greglink_tests'

setup database:
    CONFIG_FILE=/path/to/localconfig.py python setup.py

run the webapp:
    CONFIG_FILE=/path/to/localconfig.py python app.py


Writing tests
=============

Are tests are written in markdown with the '.md' file extension. Tests are then placed in the test folder (in the example above, this would be /tmp/greglink_tests). Here's an example of a test file that we will name test1.md:

~~~
---
id: test1
title: Lorem Ipsum
---

Prerequis
=========

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus dapibus egestas vehicula. Sed et sem ante. Cras ante dolor, consectetur nec cursus sit amet, consequat ut metus. Phasellus vehicula libero a nibh iaculis auctor. Nam semper placerat nisl, euismod faucibus diam ornare vel. Nulla tempus ultrices mollis. Praesent sapien massa, dictum ut interdum et, sodales et velit. Phasellus ac neque nibh, vitae fermentum odio. Suspendisse eget suscipit dolor. Nunc auctor pretium viverra. Aenean lacinia tincidunt enim ullamcorper venenatis. Nunc luctus quam eget odio facilisis dignissim. 

Execution
=========

Etape 1
-------

Fusce vitae risus sed dolor faucibus lobortis
*Resultat*: enean aliquam, justo eget ornare fermentum, sapien orci porta ipsum, in imperdiet odio dolor ac sapien

Etape 2
-------

Aliquam at dui leo, at ullamcorper arcu
*Resultat*: Cras egestas eros vel arcu faucibus vitae porta nisi tempus

Etape 3
-------

Donec sed mi id magna adipiscing semper sit amet sit amet tortor
*Resultat*: Morbi vel egestas ante
~~~

Once the test is written and copied into the test folder, you can execute the test on the web site.
