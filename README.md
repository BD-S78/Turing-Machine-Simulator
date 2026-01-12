# Turing-Machine-Simulator

This project is a fully working simulator of the logic of multitape turing machines. Write, simulate, and share custom Turing Machines that can fulfill any demand of algorithms.

## Architecture

Frontend: React/Vite application hosted on Netlify.

Backend: Python API built with FastAPI, containerized with Docker, and deployed on Render.

Database: Cloud NoSQL storage using MongoDB Atlas.

DevOps: Unified local development environment using Docker Compose.

https://b-tm-simulator.netlify.app/ - frontend


## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | React + TypeScript + Vite |
| Backend | FastAPI (Python 3.13+) |
| Database | MongoDB |
| Container | Docker Compose |


## Local Application Setup

### Prerequisites

- Docker and Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/BD-S78/Turing-Machine-Simulator.git
cd Turing-Machine-Simulator
```

### 2. Create a .env File in the Root Directory

```.env file
MONGODB_URL=your_mongodb_connection_string
VITE_API_URL=http://localhost:8000
```

### 3. Run with Docker:

```bash
docker-compose up --build
```


Frontend: http://localhost:5173

Backend API Docs: http://localhost:8000/docs

