FROM python:3.11.3-alpine3.18
LABEL mantainer="https://github.com/LuanAlmeida21"

# This environment variable is used for control if the Python should 
# save files of bytecode (.pyc) on the disk. 1 = No, 0 = Yes

ENV PYTHONDONTWRITEBYTECODE 1

# Set Python output to be displayed on the console or other output devices, 
# without being stored buffer.
# In summary, you'll see the Python outputs in real time.

ENV PYTHONUNBUFFERED 1

# Copy the folders "djangoapp" and "scripts" into the container.
COPY djangoapp /djangoapp
COPY scripts /scripts

# Go into "djangoapp" folder inside the container"
WORKDIR /djangoapp

# The port 8000 will be available for external connecations to the container.
# This is the port that we'll be using for Django.
EXPOSE 8000

# RUN executes commands on a shell inside the container to building an image.
# The result of the execution command is stored in the imagem file system as a new layer.
# Grouping the commands in a single RUN can reduce the amount of image layers and make it more efficient.

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /djangoapp/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts

# Add the scripts folder and venv/bin to the $PATH of the container.
ENV PATH="/scripts:/venv/bin:$PATH"

# Change the user to 'duser'.
USER duser

# Execute the scripts/commands.sh file.
CMD ["commands.sh"]