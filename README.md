# startupslam - all aboard the containership to confident deploys!

All aboard the container ship and anchors away! Let's set sail for adventure. 

You don't need a CSA certified floatation device for this trip, but a little preparation is sure to help.

To get the most from the workshop you'll want to download and install:
* [Docker](https://docs.docker.com/install/) 
* [Sublime Text](https://www.sublimetext.com/3) (or some other editor of your choice)
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) 

That's all you need to do before hand. The rest we'll cover in person.

**Sure, that's great, but what's in this repo?**

Great question, I'm glad you asked. This repo has three branches:
1. master - a Python Flask app
2. Dockerfile - the above flask app wrapped into a Docker image
3. DockerCompose - a further extension with a docker compose file so we can use docker-compose

The Flask app is a simple service that has two endpoints and three actions

The first returns the Fibonacci number for a given index, _n_. i.e. Fib(4)=3, where Fib(0) = 0:
* GET /fib/<int n\>/

It also does some super useful things, like tell you if some value _m_ is the _n_ th Fibonacci number:
* POST 'application/json' {"value": <int m\>} /fib/<n\>/

Or, whether _m_ is a fibonacci at all:

* POST 'application/json' {"value": <int m\>} to /fib/ 
 
 
We'll be taking this service, dockerizing it, and then connecting it to a docker instance of redis. This will give us the opportunity to see how docker works, and then touch on how docker compose makes life just a little easier.

The accompanying slides for this workshop are [here](https://docs.google.com/presentation/d/1urn-Kw59OGyloDLPF4CY7nxLtwB3sBJBcC-64fVd864/edit?usp=sharing)
