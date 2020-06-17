package PatentMR;
//
// This package demonstrates how to construct a mapper
// in a subpackage
//

import org.apache.hadoop.io.Text;
import java.io.IOException;
import java.util.StringTokenizer;

import java.util.Arrays;
import java.util.ArrayList;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Reducer;


public class CheckCitationCountReducer
    extends Reducer<LongWritable,Text,Text,Text> {

    // Counter types
    static enum CheckCitationCounter { 
	REDUCE_GOOD, REDUCE_BAD
    };


    private Text outkey = new Text();
    private Text outvalue = new Text();

    public void reduce(LongWritable key, Iterable<Text> values, Context context )
	throws IOException, InterruptedException {
	//
	// Key is the patent # and is ignored
	// We first need to find the patent reference,
	// and if there is none, do nothing
	//
	String patentInfo = null;
	int patentCitations = -1;

	ArrayList<String> citations = new ArrayList<String>();

	for (Text value : values) {

	    String[] fields = value.toString().split(",");

	    if ( fields.length > 2 ) {
		patentInfo = value.toString();
		try {
		    //
		    // The 11th field is 12th in the original data -- number of citations
		    //
		    patentCitations = Integer.parseInt( fields[11] );
		} catch( java.lang.NumberFormatException e) {
		    // leave as -1 -- bogus data
		}
	    } else {
		citations.add( value.toString() );
	    }
	}

	//
	// We might have citations for which we have no patent info...
	//
	if ( patentInfo != null ) {
	    outkey.set( key.toString() );

	    String outstr =  Integer.toString(patentCitations) + " vs "
		+ Integer.toString(citations.size());

	    if ( patentCitations == citations.size() ) {
		outvalue.set( "ok");
		context.getCounter(CheckCitationCounter.REDUCE_GOOD).increment(1);
	    } else {
		outvalue.set( "bad " + outstr );
		context.getCounter(CheckCitationCounter.REDUCE_BAD).increment(1);
	    }
	    context.write(outkey, outvalue);
	}
    }
};
