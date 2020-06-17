# Assignment #3 - Data Joins in Hadoop

## Objectives:

This lab is designed to have you do a "data join” Hadoop using a two,
single-file database. You'll be extending a Hadoop program to use
(possibly) `ChainMappers` and either `DataJoin` or a join-based solution
of your own design (which is what I would recommend). 

You also have the option of using the "streaming" interface an python code.

You start by modifying the starter code provided and extending it -
the extension will be to determine, for each patent, the number of
cited patents that originate from the same state. You will use the
description of the `acite75_99.zip` and `pat63_99.txt` files (see
`http://data.nber.org/patents` for documentation).

## Steps & Directions

Retrieve the data files from Moodle and/or git. You only need the
`acite75_99.zip` and `pat63_99.txt` files. You should unzip the
data files and place them into your HDFS file system or in a local
directory if you're using a local development machine.

The `acite75_99.txt` file contains a citation index, of the form
```
CITING CITED
```
where both CITING and CITED are integers. Each line
indicates that patent number CITING cites patent CITED.

The `pat63_99.txt` file contains the patent number, an (optional)
state in which the patent is filed and the total number of citations
made.

Your job is to augment the data in `pat63_99.txt` to include a column
indicating the number of patents cited that originate *from the same
state*. Obviously, this data can only be calculated for patents that
have originating state information and only for cited patents that
provide that information. You should generate a new file (possibly
multi-part) file that contains the augmented information.

For example, 
patent 6009554 (the last patent in pat63_99.txt) cited 9 patents. Those patents were awarded to people in
* NY, 
* IL, 
* Great Britain (no state), 
* NY, 
* NY,
* FL,
* NY,
* NY,
* NY. 

For the first part, you would produce a new data file that updates the
line:

```
6009554,1999,14606,1997,"US","NY",219390,2,,714,2,22,9,0,1,,,,12.7778,0.1111,0.1111,,
```

To be: 
```
6009554,1999,14606,1997,"US","NY",219390,2,,714,2,22,9,0,1,,,,12.7778,0.1111,0.1111,,6
```

The last value `,6` is the number of same-state citations.



To do this, you will first need do a "data join” of the citations and
the patent data - for each cited patent, you'll need to determine the
state of the cited patent. You can then use that information to
produce the augmented patent information.

It's useful to produce an intermediate table like

|Cited|State|Citing|State|
|-----|-----|------|-----|
|2134795	|None	|5654603	|OH
|2201699	|None	|5654603	|OH
|3031593	|None	|5654603	|OH
|3093764	|OH	|5654603	|OH
|3437858	|OH	|5654603	|OH
|3852137	|PA	|5654603	|OH
|3904724	|PA	|5654603	|OH

This table says that patent `3852137` is from `PA` and `5654603` is from `OH`.
You would construct this for each cited patent. From this, it's simple to determine
how many patents are self-sited for a given patent data line.

You should construct all of this as a single "Job”, using ChainMapper
to orchestrate the multiple steps. There's an example
on Stack Overflow at http://goo.gl/oDBMMP and the Hadoop class files
give descriptions as well and I've given you template code to start with.

You can also construct this using Python and I highly recommend doing that first.

## Input data files

Originally, the data files were part of the template git repo but that
causes problems with Github classroom. You should be able to download
or access the datafiles using the link
https://drive.google.com/drive/folders/1LtCL6YW-W3Ug3KAvo0gbHC3mdRXawGuo?usp=sharing
-- this will show them to you in Google Drive.

## What to hand in

You should deveop your Python and/or Java solution in the individual subdirectories.

In each case, you should include a `SOLUTION.md` file that describes the steps of your solution.
