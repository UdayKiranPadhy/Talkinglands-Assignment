FROM python:3.11

# Install PostGIS dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    postgis \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

CMD bash -c "uv sync && uv run fastapi dev --host 0.0.0.0 --port 8000 --reload"