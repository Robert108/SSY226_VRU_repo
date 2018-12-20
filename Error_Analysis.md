## Server
A server was set-up at a dedicated address by Ericsson. 

We could simply connect to it by typing:
* ssh student@40.113.6.77
* The password is: elcity999

We had a cloned repository in the server which consists of all the packages including the build files and other libraries that are needed to run the demo developed by Ericsson. However, upon following the instructions to run the demo, we encountered some errors that did not make the application successfully run.

Initially, you need to obtain a certificate from Let's Encrypt using the Docker Compose configuration (further details can be found in README.md). This, itself, caused a small problem since the port assigned to this demo (port 80) was already occupied by another application. So, we had to change the port allocation to this demo to another port (port 81) and obtain the certificate for that port.  This can be done by changing the port configuration in the docker-compose.yml file. Once you've done this, you can obtain the certificate now.

The next step in the instruction is to manage the deployment of the demo. When we tried to do this, we encountered some more errors when starting some containers, namely - dockerprod_collision-car-person_1, dockerprod_collision-bike-bus_1, dockerprod_collision-car-smv_1. The error seems to be that Docker tries to create a directory when it's supposed to create for some odd reason. So, basically, what happens is, collision-car-smv.yml, collision-car-person.yml and collision-bike-bus.yml are now "directories" instead of "files". However, when we tried to manually create these files ourselves and then try to run docker-compose, this particular error did not surface again anymore.

But, the 'Dashboard' container was not running. When we tried to manually run it using docker container start, the container just exits immediately after it starts. We tried a few fixes that we suggested online, but nothing seemed to make it work. Unfortunately, due to limited time, we decided to give up at this point and proceed further without the server.