
## Installation

Install dependencies with poetry

- Create .env with SECRET_KEY and DEBUG vars

```bash
poetry install
poe migrate
```

## Run
```bash
poe run
```

## Useful commands
```bash
poe importdata /path/to/your.csv
```

## Browse books
```bash
curl http://localhost:8000/api/v1/books?title=The%20Hobbit
curl http://localhost:8000/api/v1/books/7
```

Possible filters for /books are:
- title
- isbn
- language_code
- is_available
- original_publication_year (gte, lte)
- avg_borrowing_time (gte, lte)
- borrowing_count (gte, lte)

i.e.: 
```bash
curl http://localhost:8000/api/v1/books?original_publication_year=2000&avg_borrowing_time__gte=10
```


## Playing with the library
```bash
poe book borrow 2 "2024-04-18 00:00:00"
poe book return 2 "2024-04-30 00:00:00"
```

## Tests

```bash
poe test
poe coverage
```