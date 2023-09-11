# Use an official Python runtime as a parent image
FROM python:3.10.13-slim-bullseye
# RUN apt-get update && apt install gcc pkg-config default-libmysqlclient-dev -y
ENV PYTHONUNBUFFERED=1
# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD requirements.txt .

# Install any needed packages specified in requirementss.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 8888

# Run app.py when the container launches
# CMD ["./manage.py", "runserver"]
