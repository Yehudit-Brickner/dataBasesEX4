import pyspark
from pyspark import SQLContext
from pyspark.shell import sqlContext

conf = pyspark.SparkConf()
sc = pyspark.SparkContext.getOrCreate(conf=conf)
sqlcontext = SQLContext(sc)

# making a dataframe from the json file
df = sqlcontext.read.option("multiline", "true").json("books.json")
df.registerTempTable("df")

# fisrt question
start_with_F = sqlContext.sql("SELECT title, author, 2022-year as years_since_published FROM df WHERE author like 'F%' ")
print("showing the first question")
start_with_F.show()
print("\n \n")

# second question
# solution 1
en1 = sqlContext.sql("SELECT author, avg(pages) as avg_pages_en  FROM df WHERE language=='English' GROUP BY author")
# printing the rows of the data frame 'en1' this will show only rows if the author wrote in english
print("question 2 solution 1 ")
def f(x):
    print("author: ", x.author, "  avg_pages_eng: ", x.avg_pages_en )
en1.foreach(f)
print("\n \n")

# soltion 2
j = sqlContext.sql("SELECT * FROM ((SELECT author,avg(pages) as avg_pages_all FROM df GROUP BY author)au LEFT JOIN "
                   "(SELECT author, avg(pages) as avg_pages_en  FROM df WHERE language=='English' GROUP BY author )en "
                   "ON au.author=en.author)")
# printing the rows of the data frame 'j' this will show all rows if the author didn't write in english it will show 0
print("question 2 solution 2")
def f1(x):
    if (x.avg_pages_en!=None):
        print("author: ", x.author, "  avg_pages_eng: ", x.avg_pages_en)
    else:
        print("author: ", x.author, "  avg_pages_eng: ",0)
j.foreach(f1)