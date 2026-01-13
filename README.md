# Multi-tape Turing Machine Simulator

This project is a fully working simulator of the logic of multi-tape turing machines. Write, simulate, and share custom Turing Machines that can fulfill any demand of algorithms.

**[Live Demo](https://b-tm-simulator.netlify.app)** 
**[Backend API](https://turing-machine-simulator.onrender.com/docs)**


## Key Features
* **Multi-tape Support:** Simulate complex logic using as many tapes as necessary.
* **Community Library:** Save your machines to the database and explore recent machines created by the community.
* **Interactive UI:** Built with React for a responsive and intuitive design.


## Architecture

Frontend: React/Vite application hosted on Netlify.

Backend: Python API built with FastAPI, containerized with Docker, and deployed on Render.

Database: Cloud NoSQL storage using MongoDB Atlas.

DevOps: Unified local development environment using Docker Compose.


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

```makefile
MONGODB_URL=your_mongodb_connection_string
VITE_API_URL=http://localhost:8000
```

### 3. Run with Docker:

```bash
docker-compose up --build
```

### 4. Local Access Points

Frontend: http://localhost:5173

Backend API Documentation: http://localhost:8000/docs


## Author

Bryan Dong [Github](https://github.com/BD-S78)

## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.
