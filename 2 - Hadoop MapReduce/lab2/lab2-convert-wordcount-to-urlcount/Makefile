USER=$(shell whoami)

##
## Configure the Hadoop classpath for the GCP dataproc enviornment
##

export HADOOP_CLASSPATH=/usr/lib/jvm/java-8-openjdk-amd64/lib/tools.jar

WountCount1.jar: WordCount1.java
	hadoop com.sun.tools.javac.Main WordCount1.java
	jar cf WordCount1.jar WordCount1*.class	
	-rm -f WordCount1*.class

prepare:
	-hdfs dfs -mkdir input
	curl https://en.wikipedia.org/wiki/Apache_Hadoop > /tmp/input.txt
	hdfs dfs -put /tmp/input.txt input/file01
	curl https://en.wikipedia.org/wiki/MapReduce > /tmp/input.txt
	hdfs dfs -put /tmp/input.txt input/file02

filesystem:
	-hdfs dfs -mkdir /user
	-hdfs dfs -mkdir /user/$(USER)


stream:
	hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
	-mapper Mapper.py \
	-reducer Reducer.py \
	-file Mapper.py -file Reducer.py \
	-input input -output stream-output
