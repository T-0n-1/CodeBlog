# Code Blog

This is a simple Flask blog application with CRUD functionality for posts, and simple user authentication. This application is made for the purpose of creating test automation and is not intended for production use. This is a fork of the original FlaskBlog project that has been developed for educational purposes.

## Running Locally

### Prerequisites

- Python 3.x
- pip

### Setup

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd flask_blog
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:

   ```bash
   python init_db.py
   ```

5. Run the application:

   ```bash
   flask run
   ```

The app will be available at http://127.0.0.1:5000/

## Running with Docker

### Prerequisites

- Docker

### Build and Run

1. Build the Docker image:

   ```bash
   docker build -t flask_blog .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 5000:5000 flask_blog
   ```

The app will be available at http://127.0.0.1:5000/

---

## Project Structure

- `app.py`: Main Flask application
- `init_db.py`: Script to initialize the database
- `schema.sql`: SQL schema for the database
- `templates/`: HTML templates
- `static/`: Static files (CSS)
- `database.db`: SQLite database file

## License

MIT
