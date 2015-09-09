FROM debian-32bit:testing

# Install prerequisites
RUN apt-get update
RUN apt-get install -y --no-install-recommends wget git scons \
  build-essential binutils-dev fakeroot xz-utils valgrind python-twisted-core \
  debian-keyring debian-archive-keyring clang libexpat1-dev libqt4-dev \
  libqt4-opengl-dev libcairo2-dev libssl-dev ca-certificates

# Get Boost
ENV BOOST_PKG=boost_1_55_0 BOOST_SOURCE=$HOME/boost_1_55_0
RUN wget --quiet http://downloads.sourceforge.net/project/boost/boost/1.55.0/boost_1_55_0.tar.bz2
RUN tar xjf $BOOST_PKG.tar.bz2 $BOOST_PKG/libs/regex $BOOST_PKG/libs/filesystem $BOOST_PKG/libs/system $BOOST_PKG/libs/iostreams $BOOST_PKG/boost
RUN rm boost_1_55_0.tar.bz2

# Build V8
ENV V8_HOME=$HOME/v8
ENV PATH=$PATH:/depot_tools
RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
RUN gclient
RUN fetch --no-history v8
RUN cd v8; git checkout 3.14.5.8
RUN make -C v8 ia32.release werror=no -j$(grep -c ^processor /proc/cpuinfo)
RUN mkdir v8/lib
RUN cp v8/out/ia32.release/obj.target/tools/gyp/*.a v8/lib/

# Install buildbot 0.7.10p2-jcoffland
RUN git clone -b 0.7.10p2-jcoffland --depth=1 \
  https://github.com/CauldronDevelopmentLLC/buildbot
RUN cd buildbot; python setup.py install
