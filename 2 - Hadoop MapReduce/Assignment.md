## CSCI 5253 - Data Center Scale Computing - Lab 2

### Tasks Completed
- Hadoop Local Setup
- Running WordCount in Google Cloud Platform dataproc cluster
- Modifications to get Url Count

### Solution
My solution is implemented and tested in **Java**. The approach I followed involved 3 major steps. 
1. Implementing the **Regular Expression** to extract URLs from the webpage.
2. Changes in my **Mapper and Reducer** code to count the URLs.
3. Modifications in my **Makefile** to generate jar, run my hadoop job and download the output.

#### Regular Expression
Referring the tutorial page on Regular Expression, I created a `getLinks()` function in Java which parces the input webpage as a String and matches all the anchor tags `<a>` and the contents in them. The ouput from which is parced again to match and get URLs. The following Regular Expression is used.

Anchor tags - `"<a\\b[^>]*href=\"[^>]*>(.*?)</a>"`
URL link - `"href=\"[^>]*\">"`

The output obtained is further parsed to remove other elements in the anchor tag to extract only the link.
Example:`href=\"/wiki/IBM_General_Parallel_File_System\" class=\"mw-redirect\" title=\"IBM General Parallel File System\">IBM General Parallel File System"`
is converted to only URL
`href=\"/wiki/IBM_General_Parallel_File_System\
`
#### Mapper and Reducer
The `LinkGetter` class contained the getLinks method. The main program `UrlCount.java` contained the Mapper, Reducer and the LinkGetter class(static nested class). ***The basic idea involved reading input, getting all links from the input into a list and then counting the occurance of each link.*** The major change from Wordcount is as below.

        private final static IntWritable one = new IntWritable(1);
        private Text url = new Text();
        public void map(Object key, Text value, Context context
                        ) throws IOException, InterruptedException {
          LinkGetter linkGetter = new LinkGetter();
          List<String> links = linkGetter.getLinks(value.toString());
          for (String link : links
                 ) {
                url.set(link);
                context.write(url, one);
            }
        }
**The Reducer code remained the same since we are counting a URL in place of a Word and the data types used in the function remained same**

The Java `main()` method is updated to use the `UrlCount` class.

#### Makefile
The changes in makefile involved using the `UrlCount.java` file and `UrlCount.class` files for jar creation. 
```java
UrlCount.jar: UrlCount.java
	hadoop com.sun.tools.javac.Main UrlCount.java
	jar cf UrlCount.jar UrlCount*.class	
	-rm -f UrlCount*.class
```

### Output
The final output is written into hdfs which I copied to local file system using the below command.
`hdfs dfs -copyToLocal url-output ./url-output`
The output is split into multiple files based on the reducers used which was combined together to form output.txt. The numer of lines in output.txt provided the total unique URLs found.

Total Unique URLs found: **1554**

Total Unique URLs found without considering # references to same page such as `#cite_note-72`: **1017**

Regular Expression used: `"href=\"(//?|https?|www)[^>]*\">"`

### Steps to Run code
1. Login to Google cloud and open the Dataproc section from the navigation menu.
2. Create a cluster with your custom requirements for CPU and RAM.
3. Once Cluster is in Running state, open the cluster page, go to VM Instances Tab and SSH into the Cluster Master node.
4. Upload the UrlCount.zip by using the upload option from the top right settings panel.
5. Unzip UrlCount.zip which will contain Makefile and UrlCount.java.
6. Use the `make filesystem` command to set up the hdfs filesystem.
7. Then use the `make prepare` command to create an input directory in hdfs, curl a webpage, store contents into a file and load the files into the hfds input directory.
8. Create a jar using the `make UrlCount.jar` command.
9. Finally use `make run` to run the Hadoop MapReduce to count the number of URLs.
10. Once the jobs are completed, copy the output to local file system and zip using `make copyAndZipOutput` commad.
11. Download using the download option from the top right settings panel providing the `UrlOutput.zip` filename.
12. Lastly Delete the cluster once the outputs are obtained.
13. `Output.txt` will contain the combined output of all the reducers. The line count will provide the total unique URLs.

### Sources
- http://hadoop.apache.org/docs/stable2/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html#Example:_WordCount_v1.0
- http://www.vogella.com/tutorials/JavaRegularExpressions/article.html
- https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html
- https://stackoverflow.com/questions/5700068/merge-output-files-after-reduce-phase

*-Shreyas Gopalakrishna*
