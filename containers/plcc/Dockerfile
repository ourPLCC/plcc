# Download and extract particular version of PLCC.
# We do this in a separate stage so that Git is only installed in this stage
# and isn't in the final image.

FROM alpine:3

# Install Python 3
RUN apk add --no-cache python3~=3

# Install JDK
RUN apk add --no-cache openjdk17-jdk~=17
RUN which java
ENV JAVA_HOME="/usr/lib/jvm/default-jvm"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install bash.
RUN apk add --no-cache bash~=5

# Install bash
RUN apk add --no-cache bats~=1

# Install git
RUN apk add --no-cache git~=2

# Create separate users for PLCC and the developer.
RUN addgroup -S plcc && adduser -S plcc -G plcc
RUN addgroup -S my && adduser -S my -G my

# Copy over plcc from downloader stage.
COPY --chown=plcc:plcc . /plcc
ENV PATH="/plcc/src/plcc/bin:${PATH}"
RUN git config --global --add safe.directory /plcc
RUN git --git-dir=/plcc/.git describe --tags

# Change user to dev.
WORKDIR /workdir
RUN chown my:my /workdir
USER my:my
CMD ["/bin/bash"]
