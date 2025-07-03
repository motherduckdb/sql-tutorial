---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.2
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

<a target="_blank" href="https://colab.research.google.com/github/motherduckdb/sql-tutorial">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

# 3. Combining SQL and Python

## A. Using `duckdb` from Python

DuckDB is released with a native Python client. You can install it with a simple pip install, and there are no dependencies required.

Google Collab even has duckdb pre-installed!

We will also install a few dataframe libraries, but these are optional unless you would like to do some of your analysis outside of DuckDB!

```{code-cell}
!pip install --upgrade duckdb pandas polars pyarrow -q
```

```{code-cell}
!wget https://raw.githubusercontent.com/motherduckdb/sql-tutorial/main/data/ducks.csv -q --show-progress
!wget https://raw.githubusercontent.com/motherduckdb/sql-tutorial/main/data/birds.csv -q --show-progress
!wget https://raw.githubusercontent.com/motherduckdb/sql-tutorial/main/answers/answers_3.zip -q 
!unzip -o answers_3.zip -d answers 
```

DuckDB follows the Python DB API spec, so you can use it the same way you would use another database.
fetchall() returns a list of tuples.

```{code-cell}
import duckdb

duckdb.execute("SELECT 42 as hello_world").fetchall()
```

DuckDB also has a .sql method that has some convenience features beyond .execute. We recommend using .sql!

```{code-cell}
duckdb.sql("SELECT 42 as hello_world").fetchall()
```

## B. Writing Pandas DataFrames with DuckDB
DuckDB can also return a DataFrame directly using .df(), instead of a list of tuples!

This is much faster for large datasets, and fits nicely into existing dataframe workflows like charting or machine learning.

```{code-cell}
duckdb.sql("SELECT 42 as hello_world").df()
```

If that output looks familiar, it's because we have been using Pandas DataFrames the entire time we have been using duckdb_magic! duckdb_magic returns a dataframe as the result of each SQL query.

## C. Reading Pandas DataFrames
Not only can DuckDB write dataframes, but it can read them as if they were a table!

No copying is required - DuckDB will read the existing Pandas object by scanning the C++ objects underneath Pandas' Python objects.

For example, to create a Pandas dataframe and access it from DuckDB, you can run:

```{code-cell}
import pandas as pd
ducks_pandas = pd.read_csv('ducks.csv')

duckdb.sql("SELECT * FROM ducks_pandas").df()
```

### When to use pd.read_csv?
How would you decide whether to use Pandas or DuckDB to read a CSV file? 
DuckDB has recently invested heavily in its CSV reader and is now able to handle even messier files than Pandas!
So our recommendation would be to use DuckDB's CSV reader first (for robustness to odd CSVs, speed, and memory efficiency) and fall back to Pandas.

## D. Reading and Writing Polars and Apache Arrow

In addition to Pandas, DuckDB is also fully interoperable with Polars and Apache Arrow.

Polars is a faster and more modern alternative to Pandas, and has a much smaller API to learn.

Apache Arrow is *the* industry standard tabular data transfer format. Polars is actually built on top of Apache Arrow data types. Apache Arrow and DuckDB types are highly compatible. Apache Arrow has also taken inspiration from DuckDB's `VARCHAR` data type with their new `STRING_VIEW` type.

```{code-cell}
import polars as pl
import pyarrow as pa
import pyarrow.csv as pa_csv
```

```{code-cell}
ducks_polars = pl.read_csv('ducks.csv')
duckdb.sql("""SELECT * FROM ducks_polars""").pl()
```

```{code-cell}
ducks_arrow = pa_csv.read_csv('ducks.csv')
duckdb.sql("""SELECT * FROM ducks_arrow""").arrow()
```

```{admonition} Exercise 3.01
Read in the birds.csv file using Apache Arrow, then use the DuckDB Python library to execute a SQL statement on that Apache Arrow table to find the maximum `wing_length` in the dataset. Output that result as an Apache Arrow table.
```
```{code-cell}
# Uncomment and run to show solution
# !cat ./answers/answer_3.01.py
```

```{admonition} Exercise 3.02

Use the DuckDB Python client to return these results as a Polars dataframe.
```
```sql
SELECT
    Species_Common_Name,
    AVG(Beak_Width) AS Avg_Beak_Width,
    AVG(Beak_Depth) AS Avg_Beak_Depth,
    AVG(Beak_Length_Culmen) AS Avg_Beak_Length_Culmen
FROM 'birds.csv'
GROUP BY Species_Common_Name
```

```{code-cell}
# Uncomment and run to show solution
# !cat ./answers/answer_3.02.py
```

## 2. Using the DuckDB Relational API

In addition to SQL, you can write DuckDB queries using the built-in relational API. 
We'll see how to chain functions together to build up a query.
DuckDB will then combine that function chain together into a single query, so you still get all of DuckDB's query optimization (speed and scalability!) benefits.

The question we will build up towards answering is, "Who were the most prolific people at finding many new species of non-extinct ducks, and when did they get started finding ducks?"

<!-- TODO: Add in a few incremental steps as examples -->

The Relational API has a `read_csv` function that mirrors the Pandas function of the same name.
These methods can be called on DuckDB connection objects or the default connection using the duckb object itself.

As a note, if we wrap our relational expressions in a set of parentheses, we can organize them nicely across multiple lines. 

Here, we `filter` using an expression much like we would use in a `where` clause to only non-extinct ducks. 
The, we use `aggregate` to execute a `group by` operation, grouping by the `author` column. 
Lastly, we `order` by one of the aggregate expression columns.

```{code-cell}
duck_legends = (duckdb
  .read_csv("ducks.csv")
  .filter("extinct = 0")
  .aggregate("author, count(name) as count_name, min(year) as min_year", "author")
  .order("count_name desc")
)
duck_legends
```

You can also see the SQL that is generated using with `sql_query()` function:
```{code-cell}
print(duck_legends.sql_query())
```

Much like DuckDB can query DataFrames within SQL as if they were tables, it can also do the same for relation objects.

```{code-cell}
duckdb.sql("select * from duck_legends limit 5")
```

Technically, the `.sql` function returns a relation object as well, so you can also chain relational operations after a SQL one also!

As a silly example, we could run:

```{code-cell}
duckdb.sql("select * from duck_legends limit 5").limit(1)
```

Now we can mix and match SQL and the relational API!

```{admonition} Exercise 3.04
As an exercise, use SQL to initially pull the CSV file, but then chain together the remaining Relational operators from the `duck_legends` example above to return the same result.
```

```{code-cell}
# Uncomment and run to show solution
# !cat ./answers/answer_3.03.py
```

## 3. Using `ibis` with a DuckDB backend

### A. Introduction to Ibis and DuckDB

Another option for using DuckDB is Ibis, a powerful Python library that allows you to interact with databases using a DataFrame-like syntax. We'll also show you how to combine the SQL and Ibis so you can get the best of both worlds.

First, let's make sure you have the necessary packages installed. You can install DuckDB and Ibis using pip:

```{code-cell}
!pip install --upgrade --quiet 'ibis-framework[duckdb]'
```

We are using Ibis in interactive mode for demo purposes. This converts Ibis expressions from lazily evaluated to eagerly evaluated, so it is easier to see what is happening at each step. It also converts Ibis results into Pandas dataframes for nice formatting in Jupyter.

For performance and memory reasons, we recommend not using interactive mode in production!

We can connect to a file-based DuckDB database by specifying a file path.

```{code-cell}
import ibis
from ibis import _
ibis.options.interactive = True

con = ibis.duckdb.connect(database='whats_quackalackin.duckdb')
```

We can read in a CSV using Ibis, and it will use the DuckDB `read_csv_auto` function under the hood. This way we get both DuckDB's performance, and clean Python syntax.

```{code-cell}
ducks_ibis = ibis.read_csv('ducks.csv')
ducks_ibis
```

The result of the prior read_csv operation is an Ibis object. It is similar to the result of a SQL query - it is not saved into the database automatically.

To save the result of our read_csv into the DuckDB file, we create a table.

```{code-cell}
persistent_ducks = con.create_table('persistent_ducks', obj=ducks_ibis.to_pyarrow(), overwrite=True)
persistent_ducks
```

Now that we have a table set up, let's see how we can query this data using Ibis. Let's see how similar it feels...

We will answer the same question as with the relational API: "Who were the most prolific people at finding many new species of non-extinct ducks, and when did they get started finding ducks?"

Use the `filter` function instead of a `where` clause to choose the rows you are interested in. Ibis also uses Python's `==` comparators instead of SQL's single `=`. 

Pick your columns using the conveniently named `select` function!

The `group_by` functions matches well with the `group by` clause.

However, Ibis splits the `select` clause into the `select` function and the `aggregate` function when working with a group by. This aligns with the SQL best practice to organize your `select` clause with non-aggregate expressions first, then aggregate expressions.

```{code-cell}
duck_legends = (persistent_ducks
  .filter(persistent_ducks.extinct == 0)
  .select("name", "author", "year")
  .group_by("author")
  .aggregate([persistent_ducks.name.count(), persistent_ducks.year.min()])
  .order_by([ibis.desc("Count(name)")])
)
duck_legends
```

```{code-cell}
ibis.to_sql(duck_legends)
```

### B. Mixing and matching SQL and Ibis

If you have existing SQL queries, or want to use dialect-specific features of a specific SQL database, Ibis allows you to use SQL directly!

If you want to begin your Ibis query with SQL, you can use `Table.sql` directly.

However, we can no longer refer directly to the `persistent_ducks` object later in the expression. We instead need to use the `_` (which we imported earlier with `from ibis import _`), which is a way to build expressions using Ibis's deferred expression API. So instead of `persistent_ducks.column.function()`, we can say `_.column.function()`

```{code-cell}
duck_legends = (persistent_ducks
  .sql("""SELECT name, author, year FROM persistent_ducks WHERE extinct = 0""")
  .group_by("author")
  .aggregate([_.name.count(), _.year.min()]) # Use _ instead of persistent_ducks
  .order_by([ibis.desc("Count(name)")])
)
duck_legends
```

If you want to begin with Ibis, but transition to SQL, first give the Ibis expression a name using the `alias` function. Then you can refer to that as a table in your `Table.sql` call.

```{code-cell}
duck_legends = (persistent_ducks
  .filter(persistent_ducks.extinct == 0)
  .select("name", "author", "year")
  .group_by("author")
  .aggregate([persistent_ducks.name.count(), persistent_ducks.year.min()])
  .alias('ibis_duck') # Rename the result of all Ibis expressions up to this point
  .sql("""SELECT * from ibis_duck ORDER BY "Count(name)" desc""")
)
duck_legends
```


And there you go! You've learned:
* How to read and write Pandas, Polars, and Apache Arrow with DuckDB
* How to use DuckDB's Relational API and how to combine it with SQL
* How to use Ibis to run dataframe queries on top of DuckDB
* How to see the SQL that Ibis is running on your behalf
* How to mix and match SQL and Ibis


```{admonition} Exercise 3.04

Convert the SQL query below into an Ibis expression. You are welcome to ignore the column renaming - think of it as a "stretch-goal" if you have time! We did not cover how to do that yet.
```
```sql
SELECT
    Species_Common_Name,
    AVG(Beak_Width) AS Avg_Beak_Width,
    AVG(Beak_Depth) AS Avg_Beak_Depth,
    AVG(Beak_Length_Culmen) AS Avg_Beak_Length_Culmen
FROM 'birds.csv'
GROUP BY Species_Common_Name
```

```{admonition} Exercise 3.04

Hint: Read directly from a csv file - no need to create a persistent table!

Hint 2: Ibis uses `mean` instead of `avg`!

Hint 3: Ibis aggregate documentation: https://ibis-project.org/reference/expression-tables#ibis.expr.types.relations.Table.aggregate
```

```{code-cell}
# Uncomment and run to show solution
# !cat ./answers/answer_3.04.py
```
