CHANGELOG Suggest
=================

.. image:: https://travis-ci.org/kirankoduru/changelog.svg
    :target: https://travis-ci.org/kirankoduru/changelog

.. image:: https://coveralls.io/repos/github/kirankoduru/changelog/badge.svg?branch=master
  :target: https://coveralls.io/github/kirankoduru/changelog?branch=master

Writing CHANGELOGs can be a grueling task but git logs can help you create a *suggested* CHANGELOG. The intention of this tool is to remove some of the grunt work involved checking diffs to write CHANGELOGs.


Installation
============
You can install **changelog-suggest** through pip::

    pip install changelog-suggest


Usage
=====

Command line usage::

    usage: changelog [-h] -s START [-e END] -v VERSION [-i ISSUE]
                     [-u ISSUE_URL_PREFIX]

    Publish suggested CHANGELOG from git commits

    optional arguments:
      -h, --help            show this help message and exit
      -s START, --start START
                            Enter commit/tag/branch you want CHANGELOG from
      -e END, --end END     Enter commit/tag/branch you want CHANGELOG to. Default
                            value is set to `master` branch
      -v VERSION, --version VERSION
                            Enter new version number for the CHANGELOG
      -i ISSUE, --issue ISSUE
                            Enter issue ID pattern. Should be a regex pattern to
                            look for
      -u ISSUE_URL_PREFIX, --issue-url-prefix ISSUE_URL_PREFIX
                            Enter issue URL prefix. If your issues are on github
                            then it could be https://github.com/<username
                            >/<repository-name>/issues/<issue-number>

License
=======
MIT (See LICENSE)

Note
====
Again, this command line tool creates a suggested CHANGELOG. So use it at your discretion. It is advisable to add more information to your CHANGELOG once you have created it through this command line utility. Better advice can be found here_.

.. _here: http://keepachangelog.com/en/0.3.0/

