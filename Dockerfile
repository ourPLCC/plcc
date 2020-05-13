# Start with Alpine Linux because it is very small.
FROM alpine:3.11


# Install Python 3
RUN apk add --no-cache python3 \
  && python3 -m ensurepip \
  && pip3 install --upgrade pip setuptools \
  && rm -r /usr/lib/python*/ensurepip \
  && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
  && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
  && rm -r /root/.cache


# Install JDK
RUN apk add --no-cache openjdk11
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk/"
ENV PATH="${JAVA_HOME}/bin:${PATH}"


# Install bash
RUN apk add --no-cache bash


# Create separate users for PLCC and the developer.
RUN addgroup -S plcc && adduser -S plcc -G plcc
RUN addgroup -S me && adduser -S me -G me


# Install PLCC
COPY --chown=plcc:plcc . /plcc
ENV PATH="/plcc/Bash:${PATH}" LIBPLCC="/plcc"


# Change user to dev.
USER me:me
WORKDIR /home/me
CMD ["/bin/bash"]
