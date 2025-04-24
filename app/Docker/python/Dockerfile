FROM python:3.11

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

CMD bash -c "uv sync && uv run fastapi run"