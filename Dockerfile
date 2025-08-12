FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    g++-14 \
    clang \
    clang-tools \
    clang-tidy \
    wget \
    ccache && \
    rm -rf /var/lib/apt/lists/*

# Rename clang-18 to clang, etc.

#RUN update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-18 100
#RUN update-alternatives --install /usr/bin/clang-extdef-mapping \
#    clang-extdef-mapping /usr/bin/clang-extdef-mapping-18 100
#RUN update-alternatives --install /usr/bin/clang clang /usr/bin/clang-18 100
#RUN update-alternatives --install /usr/bin/clang-tidy \
#    clang-tidy /usr/bin/clang-tidy-18 100
#RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-14 100

# ccache shadow the compilers
RUN /usr/sbin/update-ccache-symlinks
RUN ln -s /usr/bin/ccache /usr/local/bin/clang-tidy

# Add ccache symlinks to path
ENV PATH=/usr/lib/ccache:/usr/local/bin:$PATH


# Source: https://fbinfer.com/docs/getting-started
#RUN VERSION=1.1.0; \
#    curl -sSL "https://github.com/facebook/infer/releases/download/v$VERSION/infer-linux64-v$VERSION.tar.xz" \
#    | tar -C /opt -xJ && \
#    ln -s "/opt/infer-linux64-v$VERSION/bin/infer" /usr/local/bin/infer

# Setup python virtual enviroments
RUN python3 -m venv /venv

# Set py vevn as always active
ENV VIRTUAL_ENV=/venv
ENV PATH=/venv/bin:$PATH

# Install CodeChecker and any other dependencies
RUN python3 -m pip install --upgrade pip \
&& python3 -m pip install --no-cache-dir codechecker


# Install bazelisk:
RUN VERSION=1.26.0; \
    wget "https://github.com/bazelbuild/bazelisk/releases/download/v$VERSION/bazelisk-linux-amd64" && \
    chmod +x bazelisk-linux-amd64 && \
    mv bazelisk-linux-amd64 /usr/local/bin/bazel && \
    USE_BAZEL_VERSION=6.5.0 bazel version

#CMD echo $PATH && \
#    which gcc && \
#    git clone https://github.com/furtib/codechecker_bazel.git && \
#    cd codechecker_bazel/test && \
#    git checkout ci_unit_test && \
#    echo "6.5.0" > ../.bazelversion && \
#    bazel version && \
#    python3 test.py

WORKDIR /app

CMD echo "PATH:" && \
    echo $PATH && \
    echo "==CCACHE ENV VARIABLES==" && \
    echo $CCACHE_DIR && \
    echo $CCACHE_DISABLE && \
    echo $CCACHE_COMPILERCHECK && \
    echo $CCACHE_COMPRESS && \
    echo $CCACHE_HARDLINK && \
    echo $CCACHE_LOGFILE && \
    echo $CCACHE_MAXSIZE && \
    echo "====" && \
    echo "Cacahe version:" && \
    ccache --version && \
    echo "Clang version:" && \
    clang --version && \
    echo "which clang" && \
    which clang && \
    cd /app/test && \
    echo "6.5.0" > ../.bazelversion && \
    bazel version && \
    bazel build //test:code_checker_ctu && \
    echo "CodeChecker analyzers in baze job:" && \
    cat /app/bazel-bin/test/code_checker_ctu/data/test-src-fail.cc_my.log && \
    python3 test.py
