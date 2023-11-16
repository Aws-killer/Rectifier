# Builder stage
FROM python:3.10.0-alpine as builder

# Create a non-root user
RUN adduser -D admin

# Set the working directory and adjust permissions
WORKDIR /srv
RUN chown -R admin:admin /srv && \
  chmod -R 755 /srv

# Install system dependencies
RUN apk --no-cache add \
  libu2f-dev \
  vulkan-tools \
  mesa-vulkan-radeon \
  wget \
  ffmpeg \
  curl \
  aria2 \
  ttf-liberation \
  at-spi2-atk \
  atk \
  cups-libs \
  libdrm \
  libgbm \
  gtk3 \
  nspr \
  nss \
  libu2f-host \
  vulkan-loader \
  libxcomposite \
  libxdamage \
  libxfixes \
  alsa-lib \
  libxkbcommon \
  libxrandr \
  xdg-utils \
  npm

# Copy the application code
COPY --chown=admin . /srv

# Install Node.js and npm
RUN npm install npm@latest -g && \
  npm install n -g && \
  n latest

# Print Node.js and npm versions
RUN echo "Node.js version: $(node -v)" && \
  echo "npm version: $(npm -v)"

# Install Thorium Browser or other dependencies if needed

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application Run Command
CMD ["bash", "-c", "python -m uvicorn App.app:app --host 0.0.0.0 --port 7860 & python -m celery -A App.Worker.celery worker -c 4 --loglevel=info"]

# Expose ports
EXPOSE 7860
