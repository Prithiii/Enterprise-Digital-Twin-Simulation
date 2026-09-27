# Databricks notebook source
from pyspark.sql.functions import sum

monthly_revenue = (
    silver_df
    .groupBy("Year", "Month")
    .agg(
        sum("Net_Revenue").alias("Revenue")
    )
    .orderBy("Year", "Month")
)

display(monthly_revenue)

# COMMAND ----------

spark.sql("""
SHOW TABLES IN enterprise.gold
""").show(truncate=False)