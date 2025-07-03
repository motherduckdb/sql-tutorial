# Sort to find the authors that found the most ducks (highest number of names) 
# and also calculate the first year that they found a duck.
# Start with a SQL query to pull the CSV and then chain together relational operators.

duck_legends2 = (duckdb
  .sql("FROM ducks.csv")
  .filter("extinct = 0")
  .aggregate("author, count(name) as count_name, min(year) as min_year", "author")
  .order("count_name desc")
)
duck_legends2