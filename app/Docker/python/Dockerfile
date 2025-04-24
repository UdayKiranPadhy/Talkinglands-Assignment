FROM python:3.11

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
# Remove any existing virtual environment
RUN rm -rf .venv
# Install dependencies from requirements.txt using uv
# --frozen ensures exact versions are installed
# --no-cache prevents caching to reduce image size
RUN uv sync --frozen --no-cache
# Debug - list directory contents to verify what was created
RUN ls -la /app && find /app -name ".venv" -type d

# Explicitly expose port 8000
EXPOSE 8000

# Run the application making sure to bind to 0.0.0.0
CMD [".venv/bin/fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]