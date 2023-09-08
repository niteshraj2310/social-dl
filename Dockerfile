FROM ghcr.io/anonymousx97/build_essentials:main

# adding email and username to the bot
RUN git config --global user.email "niteshraj231@outlook.com" \
    && git config --global user.name "Nitesh"

# Exposing Ports for Web Server
EXPOSE 8080 22 8022
 
# Adding Remote Container Start Command
CMD bash -c "$(curl -fsSL https://raw.githubusercontent.com/anonymousx97/Docker/main/start)"

# Installing build dependencies
# APT Packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y curl wget python git  && \
    apt-get clean

# Virtual Environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install PIP packages
COPY req.txt ./
RUN python -m pip install --no-cache-dir --upgrade pip wheel setuptools && \
    python -m pip install --no-cache-dir --upgrade -r req.txt && \
    rm -rf /tmp/*

# Working direcotry
WORKDIR /app/src

COPY . .

RUN if [ ! -d .git ] ; then \
        git clone --no-checkout "https://github.com/niteshraj2310/social-dl.git" /tmp/dirty/social-dl/ && \
        mv -u /tmp/dirty/social-dl/.git /social-dl && rm -rf /tmp/*; \
    fi

CMD ["python3","-m","app"]
