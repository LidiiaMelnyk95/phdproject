import spark
from pyspark import SparkContext

sc = SparkContext("local" , "Apriori")

df = sc.read.format("csv").load("/Users/lidiiamelnyk/Documents/GitHub/COVID-19-TweetIDs/2020-02/*.csv")

lblitems = df.map(lambda line: line.split(','))