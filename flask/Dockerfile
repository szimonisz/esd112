FROM python

# Copy all files from Dockerfile's current directory to the folder /esd112 inside the image
COPY . /esd112
# Will not work while bind volume is mounted for dev environment
RUN mkdir /esd112/app/uploads

# Set /esd112 as the working directory for the RUN, CMD commands
WORKDIR /esd112

# server will reload itself on file changes if in development mode
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Run a shell command on top of the current image
# Install all python dependencies found in the requirements.txt file using pip
# Creates a new layer by committing the results
RUN pip3 install -r requirements.txt
# The default command that will be executed when you run the docker container
#CMD ["flask","run"]
CMD ["uwsgi","uwsgi.ini"]
