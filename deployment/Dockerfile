# dockerfile that will copy the source code into the container and run the application
# use python 3.10 as the base image
FROM python:3.10-alpine

# set the working directory in the container
WORKDIR /app

# copy the source code except test directories into the container
COPY . /app

# install pip-tools
RUN pip install pip-tools

# install the dependencies
RUN pip-sync /app/requirements.txt

# expose port 8100
EXPOSE 8100

# run uvicorn to start the application
CMD ["uvicorn", "app.application:app", "--port", "8100", "--host", "0.0.0.0", "--reload"]
