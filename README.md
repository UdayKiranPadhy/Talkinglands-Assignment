# Spatial Data Platform API

A backend API service for storing, updating, and retrieving spatial data (points and polygons) using FastAPI and PostGIS.

## Features

- REST API for spatial data operations
- Support for storing, updating, and retrieving point data
- Support for storing, updating, and retrieving polygon data
- Uses PostGIS for efficient spatial queries
- Dockerized for easy deployment

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with PostGIS extension
- **Containerization**: Docker & Docker Compose

## Project Structure

```
.
├── app/                    # Application code
│   ├── api/                # API endpoints
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── database.py         # Database connection
│   └── main.py             # Application entry point
├── docker/                 # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Dockerfile for the API service
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Installation & Setup

### Prerequisites

- Docker and Docker Compose

### Running with Docker

1. Clone the repository:

```bash
git clone <repository-url>
cd spatial-data-platform
```

2. Start the services using Docker Compose:

```bash
docker-compose up -d
```

3. The API will be available at http://localhost:8000

4. API documentation is available at http://localhost:8000/docs

## API Endpoints

### Points API

- `GET /api/points` - Get all points
- `GET /api/points/{id}` - Get a point by ID
- `POST /api/points` - Create a new point
- `PUT /api/points/{id}` - Update a point
- `DELETE /api/points/{id}` - Delete a point
- `GET /api/points/within` - Get points within a specified area

### Polygons API

- `GET /api/polygons` - Get all polygons
- `GET /api/polygons/{id}` - Get a polygon by ID
- `POST /api/polygons` - Create a new polygon
- `PUT /api/polygons/{id}` - Update a polygon
- `DELETE /api/polygons/{id}` - Delete a polygon
- `GET /api/polygons/contains` - Get polygons that contain a specified point
- `GET /api/polygons/intersects` - Get polygons that intersect with a specified polygon

## License

MIT