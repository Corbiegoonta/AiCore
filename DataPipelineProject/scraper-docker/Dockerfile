FROM selenium/standalone-chrome

WORKDIR /home/app

COPY . .

USER root

RUN sudo apt-get -y upgrade
RUN sudo apt-get -y update
RUN apt install -y python3-pip

RUN pip install -r /home/app/requirements.txt

CMD ["python3", "scraper_exe.py"]

# ARG CHROME_VERSION="google-chrome-stable"
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#   && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
#   && apt-get update -qqy \
#   && apt-get -qqy install \
#     ${CHROME_VERSION:-google-chrome-stable} \
#   && rm /etc/apt/sources.list.d/google-chrome.list \
#   && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# RUN google-chrome --version | echo

# ARG CHROME_DRIVER_VERSION
# RUN if [ ! -z "$CHROME_DRIVER_VERSION" ]; \
#   then CHROME_DRIVER_URL=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_DRIVER_VERSION/linux64/chromedriver-linux64.zip ; \
#   else echo "Geting ChromeDriver binary from https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" \
#     && CFT_URL=https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json \
#     && CFT_CHANNEL="Stable" \
#     && if [[ $CHROME_VERSION == *"beta"* ]]; then CFT_CHANNEL="Beta"; fi \
#     && if [[ $CHROME_VERSION == *"unstable"* ]]; then CFT_CHANNEL="Dev"; fi \
#     && CTF_VALUES=$(curl -sSL $CFT_URL | jq -r --arg CFT_CHANNEL "$CFT_CHANNEL" '.channels[] | select (.channel==$CFT_CHANNEL)') \
#     && CHROME_DRIVER_VERSION=$(echo $CTF_VALUES | jq -r '.version' ) \
#     && CHROME_DRIVER_URL=$(echo $CTF_VALUES | jq -r '.downloads.chromedriver[] | select(.platform=="linux64") | .url' ) ; \
#   fi \
#   && echo "Using ChromeDriver from: "$CHROME_DRIVER_URL \
#   && echo "Using ChromeDriver version: "$CHROME_DRIVER_VERSION \
#   && wget --no-verbose -O /tmp/chromedriver_linux64.zip $CHROME_DRIVER_URL \
#   && rm -rf /opt/selenium/chromedriver \
#   && sudo unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
#   && rm /tmp/chromedriver_linux64.zip \
#   && sudo mv /opt/selenium/chromedriver-linux64/chromedriver /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
#   && sudo chmod 755 /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
#   && sudo ln -fs /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION /usr/bin/chromedriver


# COPY . .

# RUN pip3 install -r requirements.txt

# CMD ["python3", "scraper_exe.py"] 



# WORKDIR /app

# COPY . /app/

# RUN wget https://bootstrap.pypa.io/get-pip.py

# RUN python get-pip.py

# RUN python -m pip install -r requirements.txt

# CMD ["python", "scraper_exe.py"] 


# docker run --entrypoint=/bin/bash -it scraperf

# Microsoft Windows [Version 10.0.22621.2134]
# (c) Microsoft Corporation. All rights reserved.

# C:\Users\nickc>docker run --entrypoint=/bin/bash -it scraperf
# root@7ebc33de35e8:/app#
# root@7ebc33de35e8:/app# cd /usr/local/bin/
# root@7ebc33de35e8:/usr/local/bin# ls
# 2to3         chromedriver  f2py3.11  idle3.11  pip3     pydoc3     python-config   python3.11
# 2to3-3.11    f2py          idle      jp.py     pip3.11  pydoc3.11  python3         python3.11-config
# __pycache__  f2py3         idle3     pip       pydoc    python     python3-config  wheel
# root@7ebc33de35e8:/usr/local/bin# chromedriver
# Starting ChromeDriver 114.0.5735.90 (386bc09e8f4f2e025eddae123f36f6263096ae49-refs/branch-heads/5735@{#1052}) on port 9515
# Only local connections are allowed.
# Please see https://chromedriver.chromium.org/security-considerations for suggestions on keeping ChromeDriver safe.
# [1692296437.159][SEVERE]: bind() failed: Cannot assign requested address (99)
# ChromeDriver was started successfully.
# ^C
# root@7ebc33de35e8:/usr/local/bin# chromedriver --version
# ChromeDriver 114.0.5735.90 (386bc09e8f4f2e025eddae123f36f6263096ae49-refs/branch-heads/5735@{#1052})
# root@7ebc33de35e8:/usr/local/bin# google-chrome --version
# Google Chrome 116.0.5845.96
# root@7ebc33de35e8:/usr/local/bin# cd
# root@7ebc33de35e8:~# docker run --entrypoint=/bin/bash -it sel
# bash: docker: command not found
# root@7ebc33de35e8:~#