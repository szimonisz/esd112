FROM python

RUN apt-get update && apt-get install -y vim


# Copy all files from Dockerfile's current directory to the folder /app inside the image
COPY . /app
# Will not work while bind volume is mounted for dev environment
#RUN mkdir /app/app/uploads

# Set /app as the working directory for the RUN, CMD commands
WORKDIR /app

# the host the app will bind to (0.0.0.0)
# server will reload itself on file changes if in development mode
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Run a shell command on top of the current image
# Install all python dependencies found in the requirements.txt file using pip
# Creates a new layer by committing the results
RUN pip3 install -r requirements.txt
# The default command that will be executed when you run the docker container
# (Run flask)
#CMD ["flask","run"]
CMD ["uwsgi","uwsgi.ini"]
