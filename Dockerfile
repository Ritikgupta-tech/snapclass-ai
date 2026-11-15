# SNAPCLASS AI — Production-Grade Multi-Platform Dockerfile
# Base: Python 3.12 LTS on Debian Bookworm Slim
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Install system dependencies for dlib, librosa, and audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    curl \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create unprivileged application user
RUN groupadd -g 1001 snapclass && \
    useradd -u 1001 -g snapclass -m -s /bin/bash appuser

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip "setuptools<81.0.0" wheel && \
    pip install cmake && \
    (pip install -r requirements.txt || (pip install dlib && pip install -r requirements.txt))

# Copy application source code and configuration
COPY --chown=appuser:snapclass app.py .
COPY --chown=appuser:snapclass src/ src/
COPY --chown=appuser:snapclass .streamlit/config.toml .streamlit/config.toml
COPY --chown=appuser:snapclass docs/ docs/

USER appuser

EXPOSE 8501

# Container health probe validating Streamlit HTTP runtime
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py"]
CMD ["--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
