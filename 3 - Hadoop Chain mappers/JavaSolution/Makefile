CLASSPATH=$(shell hadoop classpath)

##/
## All of my map-reduce files in PatentMR directory.
## This is done using GNU Make function
##

MYMR = $(addsuffix .class, $(basename $(wildcard PatentMR/*)))

BASE1= PatentJoin

run: $(BASE1).jar
	hadoop jar $(BASE1).jar input output

$(BASE1).jar: $(BASE1).java $(MYMR)
	javac -classpath .:$(CLASSPATH) -Xlint $(BASE1).java
	# Set entry class to be PatentJoin
	jar cfe $(BASE1).jar $(BASE1) *.class PatentMR/*.class
	-rm -f $(BASE1)*.class

%.class: %.java
	javac -classpath .:$(CLASSPATH) $<



prepare:
	echo "Some of the following commands may fail because your"
	echo "files are already setup"
	echo "====="
	-hdfs dfs -mkdir /user
	-hdfs dfs -mkdir /user/$(USER)
	-hdfs dfs -rm -r -f /user/$(USER)/input
	-hdfs dfs -rm -r -f /user/$(USER)/output	
	-hdfs dfs -mkdir /user/$(USER)/input
	-hdfs dfs -put ../acite75_99.zip /user/$(USER)/input
	-hdfs dfs -put ../acite63_99.zip /user/$(USER)/input

clean:
	-rm -f *.class */*.class
	-rm -f *.jar
