# Builder stage
FROM python:3.10.0 as builder

RUN useradd -ms /bin/bash admin

WORKDIR /srv
RUN chown -R admin:admin /srv
RUN chmod -R 755 /srv

# Install dependencies
RUN apt-get update && \
  apt-get install -y libu2f-udev libvulkan1 mesa-vulkan-drivers wget ffmpeg

RUN apt-get install -y \
  fonts-liberation \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libatspi2.0-0 \
  libcups2 \
  libdrm2 \
  libgbm1 \
  libgtk-3-0 \
  libnspr4 \
  libnss3 \
  libu2f-udev \
  libvulkan1 \
  libxcomposite1 \
  libxdamage1 \
  libxfixes3 \
  libasound2 \
  libxkbcommon0 \
  libxrandr2 \
  xdg-utils

# Download and install Thorium Browser
RUN wget https://github.com/Alex313031/thorium/releases/download/M117.0.5938.157/thorium-browser_117.0.5938.157_amd64.deb && \
  dpkg -i thorium-browser_117.0.5938.157_amd64.deb


# Install NVM to manage Node.js versions
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

# Activate NVM in the current shell
RUN export NVM_DIR="$HOME/.nvm" && \
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
  [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Install Node.js version v18.17.0 and npm v9.6.7 using NVM
RUN nvm install 18.17.0
RUN nvm install-latest-npm

# Set the installed Node.js version as the default
RUN nvm alias default 18.17.0

USER admin

# Copy the application code
COPY --chown=admin . /srv

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# Remove Thorium Browser .deb package
RUN rm thorium-browser_117.0.5938.157_amd64.deb

# Command to run the application
CMD python -m uvicorn App.app:app --host 0.0.0.0 --port 7860 --workers 4 &  python -m celery -A App.Worker.celery worker -c 4 --loglevel=DEBUG

EXPOSE 7860