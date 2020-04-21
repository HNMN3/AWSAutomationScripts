import shutil
import os

from pyspark import SparkContext

if __name__ == "__main__":
    output_dir = 'output'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    # create Spark context with necessary configuration
    sc = SparkContext("local", "PySpark Word Count Exmaple")
    # read data from text file and split each line into words
    words = sc.textFile("input.txt").flatMap(lambda line: line.split(" "))
    # count the occurrence of each word
    wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    # save the counts to output
    wordCounts.saveAsTextFile(output_dir)
