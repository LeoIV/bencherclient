# Use python:3.11-slim as base image
FROM python:3.11-slim as build

# Set environment variables
ENV LANG=C.UTF-8 \
    PATH="/root/.local/bin:$PATH" \
    POETRY_VIRTUALENVS_PATH=/opt/virtualenvs \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    MUJOCO_PY_MUJOCO_PATH=/opt/mujoco210 \
    PYENV_ROOT="/opt/.pyenv" \
    LD_LIBRARY_PATH=/opt/mujoco210/bin:/bin/usr/local/nvidia/lib64:/usr/lib/nvidia:$LD_LIBRARY_PATH
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
ENV PATH $POETRY_HOME/bin:$PATH


# Install necessary programs
ARG PROGRAMS="git curl gcc g++ build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget \
    curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl swig \
    libglew-dev patchelf libosmesa6-dev libgl1-mesa-glx wget python3-dev"
RUN apt-get update -y && apt-get install -y $PROGRAMS

# Configure Mujoco
WORKDIR /opt
RUN wget https://github.com/google-deepmind/mujoco/releases/download/2.1.0/mujoco210-linux-x86_64.tar.gz && \
    tar -xf mujoco210-linux-x86_64.tar.gz && \
    rm mujoco210-linux-x86_64.tar.gz && \
    rm -rf /tmp/mujocopy-buildlock

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3.11 -
# Install Pyenv
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git /opt/.pyenv
# Clone BencherBenchmarks repository
RUN git clone --depth 1 https://LeoIV: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@github.com/LeoIV/BencherBenchmarks.git

# Install benchmarks
RUN for dir in /opt/BencherBenchmarks/*; do \
        if [ -d "$dir" ]; then \
            if [ -f "$dir/.python-version" ]; then \
                cd $dir && \
                pyenv install $(cat .python-version) || echo "pyenv already installed version $(cat .python-version)" && \
                PATH="$PYENV_ROOT/shims:$PATH" poetry env use $(cat .python-version); \
            fi; \
            cd $dir && \
            poetry install -v && \
            if [ -f "$dir/.python-version" ]; then \
                poetry env use system; \
            fi; \
        fi; \
    done

# Clone bencherclient repository and install
RUN git clone --depth 1 https://LeoIV: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@github.com/LeoIV/bencherclient.git && \
    cd bencherclient && \
    poetry install

# Clean up
RUN apt-get remove -y $PROGRAMS && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache/pip/* && \
    rm -rf /root/.cache/pypoetry/*

# Set the working directory to /opt/bencherclient
WORKDIR /opt/bencherclient

# Copy the entrypoint script into the Docker image
COPY docker-entrypoint.sh /docker-entrypoint.sh

# Make the script executable
RUN chmod +x /docker-entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 50051