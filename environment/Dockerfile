FROM python:3.11-slim@sha256:1042b61448fef4ba92d16a8c7eb4996d027568ce64792a7877fd88511e0af7c6

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    bash \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install standard analytical tools
RUN pip install --no-cache-dir \
    pandas==2.2.3 \
    numpy==2.2.3 \
    openpyxl==3.1.5 \
    pypdf==6.16.2 \
    reportlab==4.4.1 \
    pytest==8.3.5

# Copy input dataset files to workspace
COPY . /workspace/environment/

CMD ["/bin/bash"]
