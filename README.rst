************************************************
pmpd: Python Managed Project Deployments for git
************************************************

``pmpd`` [puhmp-eed] is a **command line interface for git deployments** that 
release engineers can use to make life easier. It is heavily influenced by 
Vincent Driessen's `branching model`_ and uses a syntax similar to `gitflow`_.  
Its goal is to simplify and streamline deployments of complex branching systems 
by making commands and actions as **human-friendly** as possible. It provides a 
simple ``pmpd`` command that allows for merging and deploying branches to any 
number of distinct servers that are **connected by a common git server** like 
`gitolite`_ and GitHub.

.. contents::
    :local:
    :depth: 1
    :backlinks: none

=============
Main Features
=============

* Expressive and intuitive syntax
* Makes continuous integration easier
* Release branches are ``pmpd`` out
* Identify conflicting feature branches before release time
* Automated ``pmpd`` deployments similar to Google's AppEngine approach
* Multi server environments supported
* Distributed branching model for large group collaborations
* Autonomous development branches for every issue
  - Still guarantees compatibility with both up and downstream
  - Developer handles merges, even with work that isn't completed yet.
* Release requirements are tightly regulated

=========
Why pmpd?
========

--------------------
git is hard to learn
--------------------

``pmpd`` is a reaction the complexities of git and the incompleteness of gitflow.  
A lot of the best criticisms of git seem to come from people who use and love
git. `Peter Lundgren`_ wrote an excellent `blog post`_ to this effect. 
`Steve Losh`_ also wrote an excellent `metaphor`_ for git's UX, comparing 
learning git to the study of Zen Koans. Git is especially hard to learn if you 
don't speak English fluently because the functionality itself can at times be 
cryptic. With 147 commands A lot of the functionality that's available in git 
is just, well, magical. The bottom line is that ``pmpd`` gives you access to some 
of that magic with fewer key strokes and a shorter learning curve.

-------------------------------------------------------------------
Development work is easier and feature branches are more autonomous
-------------------------------------------------------------------

For whatever reason developers don't always get their job done right the first 
time. In larger group projects this issue compounds as you try to manage more 
people. If everyone is working or merging work into the same repo then releasing 
collections of branches to production becomes complicated. It's insane to hold 
back working code because a minimally consequential feature fails to pass 
testing or code review. Feature branches and hotfixes need to be autonomous 
bodies of work, complete with any merging that might be required for down OR 
upstream work.

-----------------------------------------------------------------------------------
Production environments require fast and dramatic action on one to infinity servers
-----------------------------------------------------------------------------------

This is self explanatory.  When I create a release I only want to enter one 
command and I want to have insurance that my wishes have been executed on every 
development server. ``pmpd`` consolidates this functionality and uses git to do it. 
It does this without installing any extra software or configurations on your 
servers, too.

-----------------------------------------------
pmpd helps projects that are in constant triage
-----------------------------------------------

Further, some projects require the ability to partially or fully implement 
various forms of "continuous integration," a term interpreted differently 
depending on the experience and abilities available to the organization. These 
same groups might also balk at the expense of writing good unit tests and 
training less experienced talent. The time required to write sufficient unit 
tests to ensure stability before release is money better spent on lower wage 
"testers," and making people available to answer phone calls or emails from 
angry users... at least initially. To achieve these goals git really needs to 
get ``pmpd`` up so that it rolls releases forward and backward in "time" on a 
whim and without seriously effecting the development cycle.

============
Installation
============

The latest **stable version** of ``pmpd`` can always be installed or updated via 
pip:

.. code-block:: bash

    $ pip install --upgrade pmpd

=============
Configuration
=============

After installation is complete ``pmpd`` puts **.pmpd/config.json** into the root 
of your repository. You may want to add the folder to .gitignore, but leaving it 
there is also a good way to keep track of your build history and is especially 
useful if you have more than one person that's acting as a release engineer. 
pmpd.conf is used to relate servers to reference branches and to specify which 
feature branches belong in a given release. 

You must fill out **.pmpd/config.json** so that it matches the flow of your own 
**deployment** and **deployment cycles** and you'll update this file in some 
way every time a new release is ``pmpd`` out.

---------------------
Reserved branch names
---------------------

There is some automatic branch naming that goes on in ``pmpd`` that goes beyond 
just the branches that you specify in your configuration.  The following 
branches should be considered reserved and offlimits for your work.  Failure to 
observe this will end up in almost certain destruction of your branch.

Please do not try to use the following names for your branches:

* testdepends
* testalpha
* testbeta
* testpredevelop
* testdevelop
* testmaster

=====
Usage
=====

Initialize:

.. code-block:: bash

    $ pmpd

Synopsis:

.. code-block:: bash

    $ pmpd [flags] [METHOD] [BRANCH]


See also ``pmpd --help``

--------
Examples
--------

Build an alpha release based on the current state of production:

.. code-block:: bash

    $ pmpd build alpha

=========
Resources
=========

* `pmpd GitHub`_
* `pmpd PyPI`_
* `pmpd PyScape`_

====
TODO
====

* Better test coverage
* Basic Commands
    - help
    - feature start
    - feature restart
        + launch difftool against base
    - feature push
    - feature finish
    - feature reject
    - feature require
        + cannot be undone
    - hotfix start -- very distinct from the git flow model
    - hotfix push -- very distinct from the git flow model
    - hotfix finish -- very distinct from the git flow model
    - hotfix reject -- very distinct from the git flow model
    - build
        + Verify with upstream
        + Rebase? merge? Both?
        + Cleanup merged branches
* Investigate
    - pre-deployment feature conflicts
    - locate undeployed feature branches
    - locate fully integrated branches
    - cleanup loose integrated branches
    - identify deletions across branches with something akin to "git blame"
* Deployments
    - deploy
        + verify against git log
    - rollback
        + discover deployment history
        + provide the list of features/hotfixes in any given deployment
* Relate Repos
    - Support multiple repos to one ticket system "project" (Trac dispenses with the concept of "projects" in the Redmine sense)
    - Submodule Support
* ticket system integrations
    - Systems
        + Redmine
        + Trac
    - Features
        + Update ticket status (deployment status, progress status, group ownership)
        + Comments that include details about conflicts with other branches
  

============
Contributers
============

Jared Hall, `PyScape`_

.. _branching model:        http://nvie.com/git-model
.. _gitflow:               https://github.com/nvie/gitflow
.. _gitolite:              https://github.com/sitaramc/gitolite
.. _Peter Lundgren:         http://www.peterlundgren.com/
.. _blog post:              http://www.peterlundgren.com/blog/on-gits-shortcomings/
.. _Steve Losh:             http://stevelosh.com/
.. _metaphor:               http://stevelosh.com/blog/2013/04/git-koans/
.. _PyScape:                http://www.pyscape.com/pmpd
.. _pmpd GitHub:           https://github.com/jarederaj/pmpd
.. _pmpd PyPI:             https://pypi.python.org/pypi/pmpd/
.. _pmpd PyScape:           http://www.pyscape.com/pmpd
