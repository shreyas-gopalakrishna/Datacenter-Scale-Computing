# Lab 2 - Convert WordCount to UrlCount

In this lab, you're going to take an existing Hadoop application that is extensively described in the [Hadoop tutorial](http://hadoop.apache.org/docs/stable2/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html#Example:_WordCount_v1.0). You can either approach the lab as native Java-hadoop application or use the [Hadoop streaming API](https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/) to implement the lab in Python.

## Lab setup

The lab comes with a `Makefile` that provides basic steps to prepare and run the provided WordCount program. You should first insure that you can run the basic Hadoop program before starting to modify anything.

The makefile is structured assuming you're using Google's `dataproc` Hadoop cluster. You may need to modify paths if you're working in a different environment.

To test and evaluate your system, we download two WikiPedia articles. Hadoop accesses files from the HDFS file system, and we've provided a `make prepare` rule to copy the wikipedia articles to HDFS in the `input` directory. Prior to copying the files, you may need to create an HDFS entry for your user id (`make filesystem`).

### Using the Java Version
The [Hadoop tutorial](http://hadoop.apache.org/docs/stable2/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html#Usage) shows you how to run the Java program. When running your program (following the directions in the tutorial), note that the program has been named WordCount1 rather than just WordCount.

You should develop a program called `UrlCount.java` that 
Now, you're going to create a new program called ULRLister. In this program, you'll modify the Mapper to extract URL references from the documents in the input directory. This is more an exercise in using Java than using Hadoop, but it's a good preparatory step for our next assignment.

This tutorial (http://www.vogella.com/tutorials/JavaRegularExpressions/article.html ) profiles information on using the Java Regular Expression classes (`java.util.regex.Matcher and java.util.regex.Pattern`). It also provides an implementation of a class `LinkGetter` that will, when given a URL, downloads the data from the URL and produce a `List<String>` of the URL's contained therein.

You're going to modify that code to *not* download a URL -- instead, you'll provide a `String` (just like in WordCount) and extract the URL references from each string. Your mapper will then output URL references and the count of those references in the input file, more or less like WordCount.

To do this modification, you'll need to take the `LinkGetter` class, include it in the `URLLister` class and indicate that it is a "static" class (i.e. `public static class LinkGetter`). You should remove the code that fetches the URL and wraps it in a `BufferReader` -- you already have a string. This will require removing some catch blocks, but you should add a new catch ( `IllegalStateException e`) block because the Regex code throws this exception when a regex is not found. Lastly, the original code would fix relative URL references by prepending the original URL, but you should just omit that step.

Now you should be able to compile & run your code by modifying the Makefile and adding rules for `URLLister`. When you run it for the sample input (make prepare) you should find about 1,131 URL references in the two documents. Each URL should be followed by the number of times it appears in the two different files (...which were processed by two different mappers...). Most of them will appear twice, but some will appear 3, 4 or 5 times.

As you go through a edit-debug cycle, you'll need to remove the old output directory prior to re-running your application. You can do that using `hdfs dfs -rm -r /user/user/output`.

### Using Hadoop Streaming
If you're using the Hadoop streaming interface, the streaming tutorial will show you how to run the program. A sample Python version of the WordCount program is provided in files `Mapper.py` and `Reducer.py`.

In this case, you'll be doing the same task (finding all URL's embedded in the input documents) but you'll be doing it in Python and creating `URLMapper.py` and `URLReducer.py` for that task.

You could [find the URL using regular expressions](https://www.geeksforgeeks.org/python-check-url-string/) or other methods. Document what you're doing.

You code should analyze the input line-by-line just as would be done for the Java progam and the results should be the same

## What to hand in

You should create a file `SOLUTION.md` that briefly describes your solution and what software is needed for it to run. You should indicate what resources you used and anyone you worked with as described in the course collaboration policy.

You should then create a ZIP file with you code and upload it to Moodle.