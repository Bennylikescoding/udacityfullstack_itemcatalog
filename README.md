# Udacityfullstack_itemcatalog project
## Project overview:
This is the fourth project of the udacity full stack nanodegree
You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.
## This project should complete the following:
1. The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system. In this sample project, the homepage displays all current categories along with the latest added items.
2. Selecting a specific category shows you all the items available for that category.
3. Selecting a specific item shows you specific information of that item.
4. After logging in, a user has the ability to add, update, or delete item info.
5. The application provides a JSON endpoint, at the very least.
## Dependencies/Pre-requisites:
1. The virtual machine:[Vagrant](https://www.vagrantup.com/)
2. Links provided by udacity: [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
3. Virtual box toolkit: [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
## Steps to get started:
1. install Vagrant and VirtulBox
2. clone the vagrantfile from Udacity repo
3. Run `vagrant up` to run the virtual machine, then run `vagrant ssh` to login to the VM
4. Database setup: run `python database_setup.py` within this directory, which will generate the database ended with the .pyc and .db file
5. Populate database. Run `python listsofanalysis.py`
6. Run application with `python project.py`
7. Go to http://localhost/8080 to run the application
## Possible improvements:
1. Better front-end pages
2. Add "return to main page" when logout
3. Add scripts that could interact with python or R using ShinyR or other toolkit
