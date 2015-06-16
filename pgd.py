#!/usr/bin/env python
# Coding:UTF8
#
# Git-Docker env tool
#
# (c)2015 - Philippe ENTZMANN - philippe.entzmann@gmail.com
#
import os
import subprocess
import sys

print 'pgd'

USAGE = '''
pgd run : run the container for the current project/branch
pgd build : build the container for the current project/branch
'''

command = sys.argv[1] if len(sys.argv) > 1 else 'run'

#print __file__

default_image = 'phentz/devpy'
current_dir = os.getcwd()
app_name = None
git_branch = None
app_path = None
tmp_path = os.getcwd()
try:
    while tmp_path <> '':
        #TODO: disable output
        git_branch = subprocess.check_output('cd %s && git rev-parse --abbrev-ref HEAD' % tmp_path, shell=True).strip()
        app_path = tmp_path
        tmp_path, app_name = os.path.split(tmp_path)
except subprocess.CalledProcessError:
    pass

if app_name is None:
    print "This is not a git repository !"
    sys.exit(0)

docker_image = '%s-%s' % (app_name, git_branch)
#TODO: guess DockerFile
docker_file_path = os.path.join(app_path, 'container', 'dev')
extra_args = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ''

print 'App name : %s' % app_name
print 'App path : %s' % app_path
print 'Git branch : %s' % git_branch
print 'Docker image : %s' % docker_image
print 'DockerFile path : %s' % docker_file_path
print 'current_dir : %s' % current_dir
if extra_args <> '':
    print 'extra_args : %s' % extra_args


#docker_image_found = False
try:
    subprocess.check_output('docker images | grep %s' % docker_image, shell=True).strip()
    #docker_image_found = True
except:
    print 'Docker image %(docker_image)s not found, use default image %(default_image)s' % locals()
    docker_image = default_image


if command == 'build':
    #TODO: add  $1 $2 $3 $4 $5
    cmd = 'docker build -t %(docker_image)s %(docker_file_path)s' % locals()
    print cmd
    subprocess.call(cmd, shell=True)
elif command == 'run':
    # thanks to http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/
    #TODO: add  $1 $2 $3 $4 $5
    cmd = '''docker run -it --rm \
        -v %(app_path)s:/var/%(app_name)s \
        -v %(current_dir)s:/current_dir \
        -v $HOME/.Xauthority:/root/.Xauthority \
        -e DISPLAY \
        --workdir="/current_dir" \
        --net=host \
        %(docker_image)s
        ''' % locals()
    #--hostname="%(docker_image)s" \
    #print cmd
    subprocess.call(cmd, shell=True)
else:
    print USAGE
