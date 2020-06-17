USER=$(shell whoami)

##
## Configure the Hadoop classpath for the GCP dataproc enviornment
##

export HADOOP_CLASSPATH=/usr/lib/jvm/java-8-openjdk-amd64/lib/tools.jar

UrlCount.jar: UrlCount.java
	hadoop com.sun.tools.javac.Main UrlCount.java
	jar cf UrlCount.jar UrlCount*.class	
	-rm -f UrlCount*.class

prepare:
	-hdfs dfs -mkdir input
	curl https://en.wikipedia.org/wiki/Apache_Hadoop > /tmp/input.txt
	hdfs dfs -put /tmp/input.txt input/file01
	curl https://en.wikipedia.org/wiki/MapReduce > /tmp/input.txt
	hdfs dfs -put /tmp/input.txt input/file02

filesystem:
	-hdfs dfs -mkdir /user
	-hdfs dfs -mkdir /user/$(USER)

run:
	hadoop jar UrlCount.jar UrlCount input url-output

copyAndZipOutput:
	hdfs dfs -copyToLocal url-output ./url-output
	hadoop fs -getmerge url-output ./url-output/output.txt
	zip -r UrlOutput.zip url-output
