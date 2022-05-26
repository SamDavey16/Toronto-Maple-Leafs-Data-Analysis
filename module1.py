import pyspark
from pyspark.sql import SparkSession
import numpy as np
import pyspark.sql.functions as func
from os import environ
from pyspark.ml.stat import Correlation
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.ml.classification import LinearSVC
from pyspark.ml.classification import MultilayerPerceptronClassifier
import os
import sys
import itertools

# Set pyspark environment variables
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

spark = SparkSession.builder.config('spark.driver.memory','32G').config('spark.ui.showConsoleProgress', 'false').getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
df = spark.read.csv("skaters.csv", inferSchema=True,header=True)
names = df.schema.names

stringIndexer = StringIndexer(inputCol="team", outputCol="team_index").fit(df)
df = stringIndexer.transform(df)
test, training = df.randomSplit([0.3, 0.7], 20)
va = VectorAssembler(inputCols = ["icetime", "games_played", "gameScore", "season"], outputCol='sensors')
test = va.transform(test)
training = va.transform(training)

df_classifier = DecisionTreeClassifier(featuresCol="sensors", labelCol="team_index")
df_model = df_classifier.fit(training)
df_predictions = df_model.transform(test)
#df_predictions.show()
predict_accuracy1 = MulticlassClassificationEvaluator(labelCol="team_index", metricName="accuracy")
my_eval = MulticlassClassificationEvaluator(labelCol='team_index')
weightedPrecision1 = predict_accuracy1.evaluate(df_predictions, {predict_accuracy1.metricName: "weightedPrecision"})
weightedRecall1 = predict_accuracy1.evaluate(df_predictions, {predict_accuracy1.metricName: "weightedRecall"})
FalsePos = df_predictions.where((df_predictions["prediction"] == 1.0) & (df_predictions["team_index"] == 0.0)).count()
TrueNeg = df_predictions.where((df_predictions["prediction"] == 0.0) & (df_predictions["team_index"] == 0.0)).count()
print("Error rate", 1 - my_eval.evaluate(df_predictions), "Specificity %",TrueNeg / TrueNeg + FalsePos, "Sensitivity", weightedRecall1)
