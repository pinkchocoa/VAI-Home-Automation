hello instructions for set up

first u need to update ur pi

$ sudo apt get update

then check that you have at least python 3.7 installed

$ pip3 --version

you should see the version being python 3.7

then install paho mqtt that we are using

$ pip3 install paho-mqtt





u also need to clone the github repo into ur pi
it will be created as a folder in ur current repo, so make sure u are in the repo that you want it to be in

u should already have git installed when we did the linux kernel lab, otherwise do

$ sudo apt install git

then u gotta add ur credentials in for ur git acc

$ git config --global user.name "urusername"
$ git config --global user.email "theemailuuseforgithub"
$ git config --global credential.helper store
$ git clone https://github.com/pinkchocoa/1010pie.git

you will be prompted to enter ur username and password
(ps. if you can, please create a github access token and use that as ur password)

the following are commands for github, you will need to be in the right directory. 

whenever you create a new file, u need to do
$ git add filename
whenever you wanna commit your changes you need to do
$ git commit -m "ur commit message"
whenever you want to push the changes to everyone else you need to do
$ git fetch
$ git pull
$ git push

if you just want to get updates, do
$ git fetch
$ git pull

if you need other commands, do
$ git command --help
