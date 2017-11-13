# Start with a Python image.
FROM python:2.7.13

# Setting the buffer
ENV PYTHONUNBUFFERED 1
#PYTHONPATH=/path/to/whatever python some_file.py
# Install some necessary things.
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat

# Copy all our files into the image.
RUN mkdir /klaviyo
WORKDIR /klaviyo
RUN pwd
COPY . /klaviyo/
WORKDIR /klaviyo/weatheremail
RUN chmod +x manage.py
# Install our requirements.
RUN pip install -U pip
RUN pip install -Ur ../requirements.txt


# Specify the command to run when the image is run.
CMD python manage.py runserver 0.0.0.0:8000
