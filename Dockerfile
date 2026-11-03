# Use a lightweight Python 3.12 image
FROM python:3.12-slim

# Copy uv directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files first to optimize Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies from the lockfile
RUN uv sync --frozen

# Copy source code and the execution script
COPY src/ ./src/
COPY sql/ ./sql/
COPY run_elt.sh ./

# Grant execution permissions for the script
RUN chmod +x run_elt.sh

# Execute the pipeline on container start
CMD ["./run_elt.sh"]