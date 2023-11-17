# Builder stage
FROM python:3.10.0 as builder

RUN useradd -ms /bin/bash admin

WORKDIR /srv
RUN chown -R admin:admin /srv
RUN chmod -R 755 /srv

# Install dependencies
RUN apt-get update && \
  apt-get install -y libu2f-udev libvulkan1 mesa-vulkan-drivers wget ffmpeg curl aria2

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

# Copy the application code
COPY --chown=admin . /srv

# Download and install Thorium Browser

RUN apt-get update && apt-get install -y \
  software-properties-common \
  npm
RUN npm install npm@latest -g && \
  npm install n -g && \
  n latest



RUN echo npm -v
RUN node -v

#install the stuff
# RUN cd /srv/Remotion-app && npm install





# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#install unsilence
RUN pipx install unsilence




# Command to run the application
CMD python -m uvicorn App.app:app --host 0.0.0.0 --port 7860 &  python -m celery -A App.Worker.celery worker -c 4 --loglevel=info

EXPOSE 7860