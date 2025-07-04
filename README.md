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

<a target="_blank" href="https://colab.research.google.com/github/motherduckdb/sql-tutorial">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

# Learn SQL the Quacky way!

You're likely familiar with NumPy or DataFrame tools like Pandas, Polars or PyArrow for data manipulation and analysis. These are powerful tools, but as your datasets grow and your analyses become more complex, you may find yourself pushing against its limits. This is where SQL comes in.

[Structured Query Language](https://duckdb.org/docs/sql/introduction.html) (or SQL for short) is the standard language for interacting with relational databases. It's been around for decades and remains crucial in the data science toolkit.

Now, if you're ready to learn SQL, you're immediately faced with a choice: which database? A traditional OSS RDBMS like PostgreSQL or MySQL is powerful but requires server setup and configuration. SQLite is simple but struggles with analytical workloads. Cloud databases like BigQuery are great but cost money and require internet access. For learning SQL effectively, you need something that's both simple to get started with and powerful enough for real data science work.

[DuckDB](https://duckdb.org/) is an in-process SQL OLAP database management system, designed to be fast and efficient for analytical queries. It is a database that lives in-process which makes it fast, portable and easy to use and deploy. It's especially great for learning SQL because all you need to do is to download it, and it runs right on your laptop! It combines the simplicity of SQLite with the analytical power of traditional data warehouses.

But why should you care about SQL or `duckdb`?

## Why use DuckDB?

Let's start with a simple example. Imagine you're working with a climate dataset with ~50k rows, such as {Download}`washington_weather.csv<./data/washington_weather.csv>`, and you want to filter it to find all records where the observed temperature is above 25°C and precipitation is below 10 mm. With `pandas`, you might write:


```python
import pandas as pd

df = pd.read_csv('washington_weather.csv')
filtered_df = df[(df['temperature_obs'] > 25) & (df['precipitation'] < 10)]
```

This works well for small to medium-sized datasets. But what if your data doesn't fit in memory? What if you're working with a database that's constantly being updated? Or, what if you're working in an environment where Python is not available? Here's how you'd do the same thing in SQL with `duckdb`:

```sql
SELECT *
FROM read_csv('washington_weather.csv')
WHERE temperature_obs > 25 AND precipitation < 10;
```

This SQL query can work on datasets of any size, is often more efficient, and can be run close to where the data lives, reducing data transfer.

For more thoughts on why SQL is a great language to learn as a Python developer, read the [Python and SQL: Better Together](https://alex-monahan.github.io/2021/08/22/Python_and_SQL_Better_Together.html) blog post by [Alex Monahan](https://github.com/Alex-Monahan).

## Tutorial overview

Throughout this tutorial, we'll explore how SQL can complement your Python skills, enabling you to:

- Load data and perform basic operations such as filtering, sorting, grouping and adding a calculated column.
- Combine data and filter rows based on data from multiple tables
- Use SQL and Python to get the best of both worlds
- Use SQL for fast and efficient data visualization
- Share your data with your collaborators and efficiently access large amounts of data

By the end of this tutorial, you'll have a solid understanding of SQL basics, how to integrate SQL with your Python workflows, and when to choose SQL over DataFrame tools (and vice versa).

To get started, review the [Setup instructions](https://motherduckdb.github.io/sql-tutorial/setup-instructions.html). Happy querying!
