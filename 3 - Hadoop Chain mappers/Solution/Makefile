USER=$(shell whoami)
STREAMING = /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar

filesystem:
	-hdfs dfs -mkdir /user
	-hdfs dfs -mkdir /user/$(USER)

run:
	sh ./RUN-MAP-REDUCE-1

copyAndZipOutput:
	hdfs dfs -copyToLocal output ./output
	zip -r Output.zip output