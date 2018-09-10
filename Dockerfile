#Each command creates a separate layer

#Base subsquent layers on alpine:3.8
FROM alpine:3.8

#Create the /opt and /opt/app directories
RUN mkdir /opt && mkdir /opt/app

#Install python 3 and pip
RUN apk add --no-cache python3 py-pip

#Add the requirements file to /opt/app
ADD requirements.txt /opt/app

#pip install depedencies
RUN pip install -r /opt/app/requirements.txt

#Add the flask app to /opt/app
ADD app.py /opt/app/app.py

#Devleopment flask runs on port 5000. Expose.
EXPOSE 5000

#Define the comamned to execute on container start. Must bind to local loopback not localhost.
CMD flask run --host=0.0.0.0