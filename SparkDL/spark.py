#!/usr/bin/env python
#-*- coding:utf-8 -*-
from pyspark.sql import SparkSession
from pyspark import SparkContext,SparkConf
spark = SparkSession.builder.\
            master("local").\
            appName("amzone").\
            config("packages",
        "databricks:spark-deep-learning:0.1.0-spark2.1-s_2.11").\
            enableHiveSupport().\
            getOrCreate()
sc = spark.sparkContext
#sc.PACKAGE_EXTENSIONS=("databricks:spark-deep-learning:0.1.0-spark2.1-s_2.11")
from sparkdl import readImages
from pyspark.sql.functions import lit
img_dir = "data/flower"
tulips_df = readImages(img_dir + "/sunflower").withColumn("label", lit(1))
daisy_df = readImages(img_dir + "/daisy").withColumn("label", lit(0))
tulips_train, tulips_test = tulips_df.limit(40).randomSplit([0.6, 0.4])
daisy_train, daisy_test = daisy_df.limit(40).randomSplit([0.6, 0.4])
train_df = tulips_train.unionAll(daisy_train)
test_df = tulips_test.unionAll(daisy_test)
# train_df.show()

from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from sparkdl import DeepImageFeaturizer 
featurizer = DeepImageFeaturizer(inputCol="image", outputCol="features", modelName="InceptionV3")
lr = LogisticRegression(maxIter=20, regParam=0.05, elasticNetParam=0.3, labelCol="label")
p = Pipeline(stages=[featurizer, lr])
p_model = p.fit(train_df)
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

tested_df = p_model.transform(test_df)
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
print "Test set accuracy = " + str(evaluator.evaluate(tested_df.select("prediction", "label")))
