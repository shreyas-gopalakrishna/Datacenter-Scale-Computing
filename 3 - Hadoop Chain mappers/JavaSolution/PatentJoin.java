import java.io.IOException;
import java.util.*;
        
import java.lang.Integer;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import org.apache.hadoop.mapreduce.lib.chain.ChainMapper;
import org.apache.hadoop.mapreduce.lib.chain.ChainReducer;

import PatentMR.CheckCitationCountMapper;
import PatentMR.CheckCitationCountReducer;
        
public class PatentJoin {

    public static void main(String[] args) throws Exception {
	Configuration conf = new Configuration();
        
	Job job = Job.getInstance(conf, "patent check");

	//
	// Tell hadoop to send ovet the appropraiar Jar file
	//
	job.setJarByClass(PatentMR.CheckCitationCountMapper.class);

	//
	// We need to set output type of Mapper explicitly.
	// See https://stackoverflow.com/questions/12676505/hadoop-reducer-not-being-called
	//
	ChainMapper.addMapper(job,
			      CheckCitationCountMapper.class,
			      Object.class, Text.class, // input
			      LongWritable.class, Text.class, // output
			      conf);

	ChainReducer.setReducer(job,
			       CheckCitationCountReducer.class,
			       LongWritable.class, Text.class, // input
			       Text.class, Text.class, // output
			       conf);

	job.setOutputKeyClass(Text.class);
	job.setOutputValueClass(Text.class);

	FileInputFormat.addInputPath(job, new Path(args[0]));
	FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
	job.waitForCompletion(true);
    }
        
}
