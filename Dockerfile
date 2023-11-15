# Builder stage
FROM python:3.10.0 as builder

RUN useradd -ms /bin/bash admin

WORKDIR /srv
RUN chown -R admin:admin /srv
RUN chmod -R 755 /srv

# Install dependencies
RUN apt-get update && \
  apt-get install -y libu2f-udev libvulkan1 mesa-vulkan-drivers wget

# Install Thorium Browser using Snap
RUN apt-get install -y snapd && \
  snap install thorium

# Install Node.js and npm
RUN apt-get install -y nodejs npm

USER admin

# Copy the application code
COPY --chown=admin . /srv

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install JavaScript dependencies (if you have a package.json file)
COPY package*.json ./
RUN npm install

# Remove Thorium Browser .deb package
RUN rm thorium-browser_117.0.5938.157_amd64.deb

# Command to run the application
CMD uvicorn App.app:app --host 0.0.0.0 --port 7860 --workers 4 & celery -A App.Worker.celery worker -c 4 --loglevel=DEBUG
