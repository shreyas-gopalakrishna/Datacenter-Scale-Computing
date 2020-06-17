package PatentMR;
//
// Sample Mapper that is used to check if the # of citations are
// correct or incorrect
//
// The mapper reads the two input files. If the input file starts
// with "cite", we know it's a citation record, otherwise we
// know it's a patent definition. We could also use the number of
// of fields to determine the same thing, but we'll do that in
// the matching reducer
//
// The citation is stored as a "LongWritable" and we convert it to a number.
//

import org.apache.hadoop.io.Text;
import java.io.IOException;
import java.util.StringTokenizer;

import java.util.Arrays;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

import org.apache.hadoop.fs.Path;

import org.apache.hadoop.mapreduce.lib.input.FileSplit;

public class CheckCitationCountMapper
    extends Mapper<Object, Text, LongWritable, Text> {


    // Counter enum
    static enum CheckCitationCounter { 
	MAP_CITATION, MAP_PATENT
    };


    private boolean doingCite = false;

    //
    // "setup" is called when once the mapper is created on each node
    //
    protected void setup(Context context) {
	//
	// The following code determines if we're dealing with a citation
	// or the patent file
	//
	FileSplit fileSplit = (FileSplit) context.getInputSplit();
	Path path = fileSplit.getPath();
	String filename = path.getName();

	System.err.println("Got file name *" + filename + "*");

	if ( filename.startsWith("cite") ) {
	    doingCite = true;
	} else {
	    doingCite = false;
	}
    } 


    //
    // Just create one of each key/value and then set it to
    //
    private LongWritable mykey = new LongWritable();
    private Text myvalue = new Text();


    //
    // "map" is called for each record (line)
    //
    public void map(Object key, Text value, Context context )
	throws IOException, InterruptedException {

	String line = value.toString();
	String[] words = line.split(",");

	if (doingCite) {
	    try {
		mykey.set(Long.parseLong(words[0]));
		myvalue.set("y");
		context.write(mykey, myvalue);

		context.getCounter(CheckCitationCounter.MAP_CITATION).increment(1);

	    } catch (java.lang.NumberFormatException e) {
		// ignore this - bogus data
		System.out.println("ERROR-1");
	    }
	} else {
	    try {
		mykey.set(Long.parseLong(words[0]));
		String allButFirst = String.join(",",
						 Arrays.copyOfRange(words, 1, words.length)
						 );
		    
		myvalue.set(allButFirst);
		context.write(mykey, myvalue);

		context.getCounter(CheckCitationCounter.MAP_PATENT).increment(1);

	    } catch (java.lang.NumberFormatException e) {
		// ignore this - bogus data
		System.out.println("ERROR-2");
	    }
	}
	    
    }

};
