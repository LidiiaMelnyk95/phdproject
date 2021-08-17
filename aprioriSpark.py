from pyspark.sql import SparkSession

sc = SparkSession.builder.master("local[1]").appName('Apriori').getOrCreate()

df = sc.read.format("csv").load("/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-02/*.csv")

lblitems = df.rdd.map(lambda line: line.split(','))