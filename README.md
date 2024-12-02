
# Bookmark URL API

The Bookmarks API is a REST API-based project designed to help manage a collection of bookmarks URLs. With this API, you can add, read, update, and delete bookmarks.

## Feature

- CRUD Bookmark:
  - Add a bookmark.
  - View the list of bookmarks.
  - Update bookmark details.
  - Delete bookmarks.
- Authentication Endpoint using JWTs (Bearer Tokens) to protect user data.
- API documentation integrates with Swagger/OpenAPI.

## Technology Used

- **Programming Language**: Python 3.11
- **Framework**: FastAPI
- **Database**: SQLite (can be replaced as needed)

## Installation and Usage

### Prerequisites

Make sure you have installed:
- [Python 3.11](https://www.python.org/downloads/)
It is recommended to use a **virtual environment** to maintain a clean development environment.


### Installation Steps

1. Create a virtual environment::
   ```bash
   python3.11 -m venv venv
   ```
2. Clone repositori ini:
   ```bash
   git clone https://github.com/ahfay/Bookmark-API.git
   cd Bookmark-API
   ```
3. Enable the virtual environment:
- Linux/MacOS:
   ```bash
   source venv/bin/activate
   ```
- Windows:
   ```bash
   venv\Scripts\activate
   ```
4. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure environment variables: Copy the **.env.example** file to **.env**:
   ```bash
   cp .env.example .env
   ```
6. Run the app:
   ```bash
   fastapi run main.py
   ```
## API Documentation
Once the app is running, you can access the API documentation via:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

