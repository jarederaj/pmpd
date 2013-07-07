##pmpd: Git and Python Managed Project Deployments##

pmpd [git puhmp-eed] is a **command line interface for git deployments** 
that release engineers can use to make life easier. It is heavily influenced by 
[Vincent Driessen's branching model](http://nvie.com/git-model) and uses a 
syntax similar to [gitflow](https://github.com/nvie/gitflow).  Its goal is to 
simplify and streamline deployments of complex branching systems by making 
commands and actions as **human-friendly** as possible. It provides a simple 
pmpd command that allows for merging and deploying branches to any number of 
distinct servers that are **connected by a common git server** like 
[gitolite](https://github.com/sitaramc/gitolite).

###Main Features###

* Expressive and intuitive syntax
* Makes continuous integration easier
* Release branches are pmpd out
* Identify conflicting feature branches before release time
* Automated pmpd deployments similar to Google's AppEngine approach
* Multi server environments supported
* Distributed branching model for large group collaborations

###Installation###


The latest **stable version** of pmpd can always be installed or updated to 
via pip:

    $ pip install --upgrade pmpd

###Configuration###

After installation is complete pmpd puts **.pmpd/config.json** into the root 
of your repository. You may want to add the folder to .gitignore, but leaving it 
there is also a good way to keep track of your build history. pmpd.conf is used 
to relate servers to reference branches and to specify which feature branches 
belong in a given release. 

You must fill out **.pmpd/config.json** so that it matches the flow of your own 
deployments and you'll probably update this file in some way every time a new 
release is pmpd out.

###Usage###

Initialize:

    $ pmpd

Synopsis:

    $ pmpd [flags] [METHOD] [BRANCH]

See also *pmpd --help*

####Examples####

Build an alpha release:

    $ pmpd build alpha

###Resources###

* [pmpd GitHub](https://github.com/jarederaj/pmpd)
* [pmpd PyPI](https://pypi.python.org/pypi/pmpd/)
* [pmpd PyScape](http://pyscape.com/pmpd)
