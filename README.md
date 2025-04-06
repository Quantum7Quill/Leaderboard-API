# Leaderboard-API

Leaderboard-API is a Django-based application programming interface (API) designed to manage and retrieve leaderboard data. It allows users to interact with a leaderboard system, where they can view and update their scores and positions.

## Features

- Submit scores for users.
- Retrieve the rank of a specific user.
- Get the top leaderboard entries.
- Rate limiting to prevent abuse of the API.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Docker (for containerized deployment)
- PostgreSQL (as the database)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/vivekkumar/Leaderboard-API.git
   cd Leaderboard-API
   ```
### Using Docker
1. **Build the Docker image:**
`docker-compose build`
2. **Run the Docker containers:**
`docker-compose up`

### API Endpoints
[API Doc](https://documenter.getpostman.com/view/42225946/2sB2cUBiEX)
- Submit Score: POST /api/leaderboard/score
- Get Rank: GET /api/leaderboard/rank/<user_id>/
- Get Leaderboard: GET /api/leaderboard/top

### Rate Limiting
The API implements rate limiting to prevent abuse. The default throttle rates are:
User: 100 requests per minute
IP: 5 requests per day

### Testing
To run the tests, use the following command:
`python manage.py test`

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements.