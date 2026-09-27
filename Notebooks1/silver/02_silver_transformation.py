# Databricks notebook source
bronze_df = spark.table("enterprise.bronze.sales_raw")

bronze_df.printSchema()

# COMMAND ----------

silver_df = silver_df.withColumn(
    "Net_Revenue",
    col("Sales") * (1 - col("Discount"))
)

# COMMAND ----------

from pyspark.sql.functions import year, month, quarter

silver_df = silver_df.withColumn(
    "Year",
    year("Order_Date")
)

silver_df = silver_df.withColumn(
    "Month",
    month("Order_Date")
)

silver_df = silver_df.withColumn(
    "Quarter",
    quarter("Order_Date")
)

# COMMAND ----------

spark.sql("""
SELECT *
FROM enterprise.silver.sales_clean
LIMIT 10
""").show()