## CSCI 5253 - Data Center Scale Computing - Lab 3

Chain Mappers to accomplish a Data join

### Task Completed
-  Calculating and adding the number of patents cited that originated from the same state

### Solution
My solution is implemented and tested in **Python**. The approach I followed involved 3 major steps. 
1. Map-Reduce-1 to get the state of Citing.
2. Map-Reduce-2 to get the state of Cited.
3. Map-Reduce-3 to count the total citations from the same state
**Output can be accomplished with only 2 Map Reduce steps too.

#### Map-Reduce-1
**Input**: acite75_99.txt and pat63_99.txt. Value size used to differentiate between cite data and patent data throughout the program. Finding the state of citing by using the patent info. Mapper choose citing as key and rest as value. Reducer adds the state of citing since citing and info will be available in the same reducer.
                    
Key  | Value
------------- | -------------
6009532  | 5621901
6009533  | 5621901
6009532  | 1999,14606,1997,"US","CA",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,
6009533  | 1999,14606,1997,"US","CO",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,
5621901  | 1999,14606,1997,"US","CA",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,

**Output**:
                    
Key  | Value
------------- | -------------
6009532  | "CA",5621901
6009532  | 1999,14606,1997,"US","CA",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,
6009533  | "CO",5621901
6009533  | 1999,14606,1997,"US","CO",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,
5621901  | 1999,14606,1997,"US","CA",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,


#### Map-Reduce-2
**Input**: From output of Map-reduce-1. Finding the state of cited by using the patent info. Mapper choose cited as key and rest info created as value. Reducer adds the state of cited.

**Output**:
                    
Key  | Value
------------- | -------------
5621901  | "CA", 6009532, "CA"
5621901  | "CA", 6009533, "CO"
5621901  | 1999,14606,1997,"US","CA",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,
6009532  | 1999,14606,1997,"US","CA",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,
6009533  | 1999,14606,1997,"US","CO",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,

#### Map-Reduce-3
**Input**: From output of Map-reduce-2. Data of all citing are passed to same mapper and same state count for each cited patent is calculated. The calculated count is appended at end of patent info which is desired output.

**Output**:
                    
Key  | Value
------------- | -------------
6009532  | 1999,14606,1997,"US","CA",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,,1
6009533  | 1999,14606,1997,"US","CO",763248,2,,714,2,22,11,0,1,,0.8264,,2.7273,0,0,,,0


##### Shell script to run Map-reduce streaming API jobs one after another to create chain mapper was implemented.


### Output
The final count of same state citations for few of the patents are as given below.
6009554 ,1999,14606,1997,"US","NY",219390,2,,714,2,22,9,0,1,,,,12.7778,0.1111,0.1111,,,8
6009345,1999,14606,1997,"US","CA",713506,2,,604,3,32,5,0,1,,0,,4.6,0.6,0.6,,,4
6009541,1999,14606,1997,"US","CA",722315,2,,714,2,22,155,0,1,,0.8503,,2.6968,0.0132,0.0129,,,43
5959466,1999,14515,1997,"US","CA",5310,2,,326,4,46,159,0,1,,0.6186,,4.8868,0.0455,0.044,,,125


### Steps to Run code
1. Login to Google cloud and open the Dataproc section from the navigation menu.
2. Create a cluster with your custom requirements for CPU and RAM.
3. Once Cluster is in Running state, open the cluster page, go to VM Instances Tab and SSH into the Cluster Master node.
4. Upload the Solution.zip by using the upload option from the top right settings panel.
5. Unzip Solution.zip which will contain Makefile scripts and required Python map-reduce files.
6. Use the `make filesystem` command to set up the hdfs filesystem.
7. Then copy input files into a folder named ''input" in hfds input directory.
8. Use `make run` to run the Chain MapReduce jobs which computes the output.
10. Once the jobs are completed, copy the output to the local file system and zip using `make copyAndZipOutput` command.
11. Download using the download option from the top right settings panel providing the `Output.zip` filename.
12. Lastly, Delete the cluster once the outputs are obtained.
13. `Output` folder will contain the combined output of all patents with the count of same state citations.

### Sources
- https://blog.matthewrathbone.com/2016/02/09/python-tutorial.html


*-Shreyas Gopalakrishna*

