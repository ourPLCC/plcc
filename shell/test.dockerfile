FROM debian

ARG PYTHON_VERSION=3
ARG JAVA_VERSION
ARG USERNAME=tester
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update \
    && apt-get install -y \
        build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev curl \
        libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
        git curl bash zip sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
ENV HOME="/home/$USERNAME"
WORKDIR $HOME
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN pyenv install ${PYTHON_VERSION} && pyenv global ${PYTHON_VERSION}

RUN bash -c 'curl -s https://get.sdkman.io | bash'
RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && sdk install java $JAVA_VERSION"

COPY --chown=$USERNAME:$USERNAME . $HOME/.plcc
ENV PATH="$HOME/.plcc/src:${PATH}" LIBPLCC="$HOME/.plcc/src"
