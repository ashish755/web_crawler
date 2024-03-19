FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    wget \
    && apt-get clean

COPY ./requirements.txt ./requirements.txt

# Install required dependencies (wget, tar)
RUN apt-get update && apt-get install -y wget tar && rm -rf /var/lib/apt/lists/*

# Download Firefox tarball
RUN wget -O firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"

# Extract Firefox tarball to /opt directory
RUN tar xjf firefox.tar.bz2 -C /opt/

# Set symbolic link for Firefox binary
RUN ln -s /opt/firefox/firefox /usr/bin/firefox

# Clean up downloaded tarball
RUN rm firefox.tar.bz2

# Set the entrypoint
ENTRYPOINT ["firefox"]

# Download the latest GeckoDriver release for Linux
RUN wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz && \
    tar -xzf geckodriver.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver.tar.gz

COPY . .

RUN find / -name firefox
CMD ["python", "./web_crawler.py"]