# Expense Tracker

Record expenses, summarize totals by category, and store records in JSON.

Requires Python 3.10+; no external packages.

## Run

```shell
python app.py add 1500 Food --note lunch
python app.py summary
```

Run these commands inside this project's folder. On Windows, replace `python` with `py` if necessary.

## Test

```shell
python -m unittest -v
```

This is a learning project. Local JSON data is saved in the current working directory where applicable.
