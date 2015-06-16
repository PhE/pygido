# pygido

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
  Each branch has its own dependencies. I want 2 different docker image
  ready to launch in a single command.


# Install

You need Python.

Symlink the pgd.py script.

# Usage

Run the container for the current project/branch
```
pgd run
```

Build the container for the current project/branch
```
pgd build
```
