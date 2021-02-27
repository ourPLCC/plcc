# Download and extract particular version of PLCC.
# We do this in a separate stage so that Git is only installed in this stage
# and isn't in the final image.

ARG ALPINE_IMAGE=alpine:3.12
ARG ALPINE_BASH_PACKAGE=bash~=5.0
ARG ALPINE_PYTHON_PACKAGE=python3~=3.8
ARG ALPINE_JAVA_PACKAGE=openjdk11-jdk~=11.0

# Bash unit testing framework
ARG ALPINE_BATS_PACKAGE=bats~=1.2

FROM ${ALPINE_IMAGE}
COPY . /plcc

# Install Python 3
ARG ALPINE_PYTHON_PACKAGE
RUN apk add --no-cache ${ALPINE_PYTHON_PACKAGE} \
  && python3 -m ensurepip \
  && pip3 install --upgrade pip setuptools \
  && rm -r /usr/lib/python*/ensurepip \
  && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
  && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
  && rm -r /root/.cache

# Install JDK
ARG ALPINE_JAVA_PACKAGE
RUN apk add --no-cache ${ALPINE_JAVA_PACKAGE}
RUN which java
ENV JAVA_HOME="/usr/lib/jvm/default-jvm"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install bash.
ARG ALPINE_BASH_PACKAGE
RUN apk add --no-cache ${ALPINE_BASH_PACKAGE}

# Install bash
ARG ALPINE_BATS_PACKAGE
RUN apk add --no-cache ${ALPINE_BATS_PACKAGE}

# Create separate users for PLCC and the developer.
RUN addgroup -S plcc && adduser -S plcc -G plcc
RUN addgroup -S my && adduser -S my -G my

# Copy over plcc from downloader stage.
COPY --chown=plcc:plcc . /plcc
ENV PATH="/plcc/src:${PATH}" LIBPLCC="/plcc/src"

# Change user to dev.
WORKDIR /workdir
RUN chown my:my /workdir
USER my:my
CMD ["/bin/bash"]
