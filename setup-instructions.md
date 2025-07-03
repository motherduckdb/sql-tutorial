---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Setup instructions

Welcome! It's officially SQL-o-clock!

For the initial, SQL-only sections of this tutorial, please install the DuckDB command line interface (CLI) and load the tutorial notebooks following the steps below:

## Sections 1 and 2

1. Follow the DuckDB CLI installation instructions for your OS and CPU
2. Create a these folders in your user directory:
  * MacOS and Linux: `~/.duckdb/extension_data/ui`
  * Windows: `%userprofile%\.duckdb\extension_data\ui`
3. Copy the tutorial notebook data stored in the file [ui.db](https://github.com/motherduckdb/sql-tutorial/raw/refs/heads/main/ui.db) into that folder
  * Note: If you have already used the DuckDB Local UI, rename the existing ui.db and ui.db.wal before copying over the new ui.db from the link above.
4. Ensure that duckdb is added to your path, or navigate to the folder where you saved the DuckDB CLI
5. Run `duckdb -ui` (or `./duckdb -ui` if it is not on your path), and we are off and flying!
  * Your browser should automatically open to `http://localhost:4213/` - go there to see the UI!

## Section 3

For the sections that cover combining SQL and Python, see the installation instructions in section 3.

## Section 4

In preparation for section 4, please [sign up for a free account with MotherDuck](https://app.motherduck.com/?auth_flow=signup)!
