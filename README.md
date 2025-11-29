# Rave Ramen Reviews 🍜

A RESTful API for managing and querying ramen reviews built with Python and Flask.

## Description

Rave Ramen Reviews is a RESTful API that provides programmatic access to ramen review data. Users can create, read, update, and delete ramen reviews through simple API endpoints. The application uses SQLite for data storage and supports bulk operations from CSV files, making it easy to manage large datasets of ramen reviews.

## Features

- Create, Read, Update, and Delete (CRUD) operations for ramen reviews
- Bulk import reviews from CSV files
- Search reviews by multiple criteria (Brand, Country, Type, Rating, etc.)
- Sort search results by any field
- Keyword-based search for finding specific ramen types
- RESTful API design with proper HTTP status codes
- Built-in API documentation page

## Technologies Used

- Python 3
- Flask (Web Framework)
- Flask-RESTful (REST API Extension)
- SQLite (Database)
- HTML/CSS/JavaScript (Documentation UI)
- Gunicorn (WSGI Server for deployment)

## Installation

```bash
# Clone the repository
git clone https://github.com/bryanseah234/ramenreviews.git

# Navigate to project directory
cd ramenreviews

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the application
python main.py
```

The API will be available at `http://127.0.0.1:5000`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/createone` | GET | Create a new database and table |
| `/api/addone` | PUT | Add a single ramen review |
| `/api/addmany` | GET | Import reviews from CSV file |
| `/api/searchsome` | PUT | Search reviews with filters |
| `/api/selectall` | GET | Get all ramen reviews |
| `/api/editsome` | PUT | Update existing reviews |
| `/api/deletesome` | PUT | Delete specific reviews |
| `/api/deleteall` | GET | Delete all reviews |

Visit `/documentation` for detailed API documentation.

## Demo

~~https://rave-ramenapi.herokuapp.com~~ (Heroku free tier discontinued)

## Disclaimer

1. FOR EDUCATIONAL PURPOSES ONLY
2. USE AT YOUR OWN DISCRETION

## License

MIT License

---

**Author:** <a href="https://github.com/bryanseah234">bryanseah234</a>
