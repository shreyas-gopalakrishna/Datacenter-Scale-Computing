# Python starter code

The following code is a streaming map-reducer written in Python.
It performs a single map-reduce phase.
The mapper processes either the citations or the patent data.
In each case, it outputs the patent number which is used by the reduce.
For patent records, it also outputs all the patent information; for citations it just outputs a 'y'.

The reducer examines all the records for the same patent.
It counts the citations and compares that to the expected number of citations in the patent data.

If a patent has patent data, then "ok" is reported if the patent numbers match, otherwise "bad" and the expected and found citations.

You should find all patents are "ok" when you run the output.

## Python details

Because there is no ChainMapper when using streaming, you'll need to need to write multiple Mapper/Reducer files.

You should leave your final output in 'output'


