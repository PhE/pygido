pygido
=========

My PYthon GIt DOcker integrated tool.

A simple tool to ease the combinated use of Python, Git and Docker.

Here are the basic use cases I would like to address with this tool :

* I want to challenge a new idea. I create an empty directory and
  drop some data files.
  I want to be able to start coding in a IPython notebook with all my
  usefull tools already available (pandas)

* I just checkout a git repo of one of my project and I want to be able
  to run a docker container with all my dev tools in a single command.

* I work on 2 different branches of the same project.
  Each branch has its own dependencies. I want 2 different docker images
  ready to launch in a single command.

* The laptop I am working on is not mine. I want to be able to write code
  with a graphical IDE at a minimal setupcost.


Install
-------------

You need Python.

Symlink the pgd.py script ::

  sudo ln -s `pwd`/pygido/pgd.py /usr/bin/pgd


Basic usage
--------------

Build the container for the current project/branch ::

  pgd build


Run the container for the current project/branch ::

  pgd run


Multiple Dockerfile
------------------------

When switching to a different Dockerfile, you must rebuild the image :

  pgd build --DockerfilePath container/prod

Then run it :

  pgd run


TODO
---------

* add more use cases
* add conf file to set fallback docker image
* integrate docker machine (to work remotly)
* integrate docker compose (to set up multiple container at once)
