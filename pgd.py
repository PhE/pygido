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
import argparse

print 'pgd'
parser = argparse.ArgumentParser(prog='pgd', description='Python Git Docker simple integrator',
        formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("command", choices=['run', 'build', 'info', 'bootstrap'], default = 'run',
        help='''Action to perform :
%(prog)s run : run the container for the current project/branch
%(prog)s build : build the container for the current project/branch
%(prog)s bootstrap : create a basic Dockerfile
%(prog)s info : output info only
''')
parser.add_argument('-d', '--dry', action='store_true',
        help="No action. Show the actions that would occur but do not actually start or build a container.")
args = parser.parse_args()


#command = sys.argv[1] if len(sys.argv) > 1 else 'run'

#print __file__
FNULL = open(os.devnull, 'w')

default_image = 'phentz/devpy' #:latest ?
current_dir = os.getcwd()
app_name = None
git_branch = None
app_path = None
tmp_path = os.getcwd()
try:
    while tmp_path <> '':
        #TODO: disable output
        git_branch = subprocess.check_output(
                'cd %s && git rev-parse --abbrev-ref HEAD' % tmp_path,
                stderr=FNULL, shell=True).strip().lower()
        app_path = tmp_path
        tmp_path, app_name = os.path.split(tmp_path)
except subprocess.CalledProcessError:
    pass
if app_name is None:
    app_path = current_dir

#output = git_branch = subprocess.check_output('git rev-parse --is-inside-work-tree',
#    stderr=FNULL, shell=True).strip().lower())
#print output

if app_name:
    docker_image = '%s-%s' % (app_name.lower(), git_branch)
else:
    docker_image = default_image
#TODO: guess DockerFile
docker_file_path = os.path.join(app_path, 'container', 'dev')
if not os.path.exists(os.path.join(docker_file_path,'Dockerfile')):
    docker_file_path = current_dir #app_path
    if not os.path.exists(os.path.join(docker_file_path, 'Dockerfile')):
        docker_file_path = None
#extra_args = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ''

print 'App name : %s' % app_name
print 'Git branch : %s' % git_branch
print 'Docker image : %s' % docker_image
print 'DockerFile path : %s' % docker_file_path
#if extra_args <> '':
#    print 'extra_args : %s' % extra_args


try:
    subprocess.check_output('docker images | grep %s' % docker_image, shell=True).strip()
except:
    if args.command == 'run':
        print 'Docker image %(docker_image)s not found, use default image %(default_image)s' % locals()
        docker_image = default_image


#TODO: add  $1 $2 $3 $4 $5
cmd_build = 'docker build -t %(docker_image)s %(docker_file_path)s' % locals()
# thanks to http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/
#TODO: add  $1 $2 $3 $4 $5
cmd_run = '''docker run -it --rm \
-v %(app_path)s:/var/myapp \
-v %(app_path)s:/var/%(app_name)s \
-v %(current_dir)s:/current_dir \
-v $HOME/.Xauthority:/root/.Xauthority \
-e DISPLAY \
--workdir="/current_dir" \
--net=host \
%(docker_image)s''' % locals()

if args.command == 'build':
    if docker_file_path is None:
        print 'Dockerfile not found !'
        sys.exit(0)
    print 'exec :', cmd_build
    if not args.dry:
        subprocess.call(cmd_build, shell=True)
elif args.command == 'run':
    #--hostname="%(docker_image)s" \
    print 'exec :', cmd_run
    if os.path.exists(os.path.join(app_path, 'container', 'dev', 'autoexec_docker')):
        print 'exec autoexec_docker :', cmd_run+" sh -c '/sbin/setuser alan /current_dir/container/dev/autoexec_docker'"
        if not args.dry:
            #subprocess.call(cmd_run, shell=True)
            subprocess.call(cmd_run+" sh -c '/sbin/setuser alan /current_dir/container/dev/autoexec_docker'", shell=True)
    else:
        print 'exec default :', cmd_run
        if not args.dry:
            subprocess.call(cmd_run, shell=True)

elif args.command == 'bootstrap':
    # Create the default Dockerfile path
    if not os.path.exists(docker_file_path):
        print 'Creating folder %s ...' % docker_file_path
        os.makedirs(docker_file_path)
    # Create the default Dockerfile
    docker_file = os.path.join(docker_file_path, 'Dockerfile')
    if not os.path.exists(docker_file):
        print 'Creating file %s ...' % docker_file
        with open(docker_file, 'w') as f:
            f.write('''FROM %s:latest\n''' % default_image)
    else:
        print 'A Dockerfile already exists in  %s !' % docker_file
elif args.command == 'info':
    print 'App path : %s' % app_path
    print 'current_dir : %s' % current_dir
    print 'Docker commands :\n'
    print cmd_build
    print cmd_run
