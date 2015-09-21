FROM debian:testing

# Deps
RUN apt-get update
RUN apt-get install -y debian-keyring debian-archive-keyring adduser sudo \
  libgl1-mesa-swx11

# Create user buildbot
ENV USER=buildbot
RUN adduser --uid 1000 $USER --disabled-password --gecos ""
RUN echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER
RUN chmod 0440 /etc/sudoers.d/$USER

# Qt needs this
ENV QT_X11_NO_MITSHM 1

# Install package
ADD http://192.168.10.15/builds/release/camotics/debian-testing-64bit/v1.0/latest/camotics_1.0.0_amd64.deb /
RUN apt-get update
RUN dpkg -i /camotics_1.0.0_amd64.deb || apt-get install -yf

USER $USER
ENV HOME /home/$USER
CMD /usr/bin/camotics
