FROM python:3.12-alpine

# Set working directory
WORKDIR /rag_finance

# Install system dependencies and UV
RUN apk add --no-cache \
    cargo \
    curl \
    gcc \
    libffi-dev \
    musl-dev \
    openssl-dev \
    python3-dev \
    rust \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p rag_finance/data

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "fastapi", "dev", "rag_finance/api/routes.py", "--host", "0.0.0", "--port", "8000"]
