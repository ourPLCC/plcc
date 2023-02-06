# Download and extract particular version of PLCC.
# We do this in a separate stage so that Git is only installed in this stage
# and isn't in the final image.

FROM alpine:3.14

# Install Python 3
RUN apk add --no-cache python3~=3.9 \
  && python3 -m ensurepip \
  && pip3 install --upgrade pip setuptools \
  && rm -r /usr/lib/python*/ensurepip \
  && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
  && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
  && rm -r /root/.cache

# Install JDK
RUN apk add --no-cache openjdk11-jdk~=11.0
RUN which java
ENV JAVA_HOME="/usr/lib/jvm/default-jvm"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install bash.
RUN apk add --no-cache bash~=5.1

# Install bash
RUN apk add --no-cache bats~=1.3

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
