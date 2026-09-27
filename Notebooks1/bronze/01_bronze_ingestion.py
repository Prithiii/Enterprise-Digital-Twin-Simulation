# Databricks notebook source
spark.sql("""
SELECT *
FROM enterprise.bronze.sales_raw
LIMIT 5
""").show()

# COMMAND ----------

spark.sql("SHOW CATALOGS").show(truncate=False)

# COMMAND ----------

sales_df.show(5)

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

sales_df.printSchema()