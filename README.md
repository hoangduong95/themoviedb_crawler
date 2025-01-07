# TMDB Movies Scrapy Project

This project is a Scrapy spider designed to scrape movie data from The Movie Database (TMDB) website. The spider extracts various details about movies, including their title, release year, genres, runtime, user score, cast, crew, and more.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/tmdb_movies_scrapy.git
    cd tmdb_movies_scrapy
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run the spider, use the following command:
```sh
scrapy crawl TMDB_Movies
