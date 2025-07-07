FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    python3-venv \
    software-properties-common \
    unzip \
    lsb-release \
    gnupg \
    ca-certificates \
    g++-14 \
    clang-18 \
    clang-tools-18 \
    clang-tidy-18 \
    cppcheck && \
    rm -rf /var/lib/apt/lists/*

# Rename clang-18 to clang, etc.

RUN update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-18 9999
RUN update-alternatives --install /usr/bin/clang-extdef-mapping \
    clang-extdef-mapping /usr/bin/clang-extdef-mapping-18 9999
RUN update-alternatives --install /usr/bin/clang clang /usr/bin/clang-18 9999
RUN update-alternatives --install /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-18 9999
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-14 9999

# Source: https://fbinfer.com/docs/getting-started
RUN VERSION=1.1.0; \
    curl -sSL "https://github.com/facebook/infer/releases/download/v$VERSION/infer-linux64-v$VERSION.tar.xz" \
    | tar -C /opt -xJ && \
    ln -s "/opt/infer-linux64-v$VERSION/bin/infer" /usr/local/bin/infer

# Setup python virtual enviroments
RUN python3 -m venv /venv
ENV VIRTUAL_ENV=/venv
ENV PATH=/venv/bin:$PATH

# Install CodeChecker and any other dependencies
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install --no-cache-dir codechecker

# Install bazelisk:
RUN VERSION=1.26.0; \
    wget "https://github.com/bazelbuild/bazelisk/releases/download/v$VERSION/bazelisk-linux-amd64" && \
    chmod +x bazelisk-linux-amd64 && \
    mv bazelisk-linux-amd64 /usr/local/bin/bazel

