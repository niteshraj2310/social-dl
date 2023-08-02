FROM ghcr.io/anonymousx97/build_essentials:main

# adding email and username to the bot
RUN git config --global user.email "niteshraj231@outlook.com" \
    git config --global user.name "niteshraj2310"

# Exposing Ports for Web Server
EXPOSE 8080 22 8022
 
# Adding Remote Container Start Command
CMD bash -c "$(curl -fsSL https://raw.githubusercontent.com/anonymousx97/Docker/main/start)"
