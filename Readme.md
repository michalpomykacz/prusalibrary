
## Installation

Install dependencies with poetry

- Create .env with SECRET_KEY and DEBUG vars

```bash
poetry install
poe migrate
```

## Useful commands
```bash
poe importdata /path/to/your.csv
```

## Playing with the library
```bash
poe book borrow 2 "2024-04-18 00:00:00"
poe book return 2 "2024-04-30 00:00:00"
```

## Tests

```bash
poe test
```