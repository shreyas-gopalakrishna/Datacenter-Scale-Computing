import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import javax.naming.Context;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class UrlCount {

  public static class TokenizerMapper
       extends Mapper<Object, Text, Text, IntWritable>{

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
  }

  public static class IntSumReducer
       extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "url count");
    job.setJarByClass(UrlCount.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
  
  
  
  public static class LinkGetter {
    private Pattern htmltag;
    private Pattern link;

    public LinkGetter() {
        htmltag = Pattern.compile("<a\\b[^>]*href=\"[^>]*>(.*?)</a>");
        link = Pattern.compile("href=\"[^>]*\">");
    }

    public List<String> getLinks(String page) {
        List<String> links = new ArrayList<String>();
        try {

            Matcher tagmatch = htmltag.matcher(page);
            while (tagmatch.find()) {
                Matcher matcher = link.matcher(tagmatch.group());
                matcher.find();
                String link = matcher.group().replaceFirst("href=\"", "")
                        .replaceFirst("\">", "")
                        .replaceFirst("\"[\\s]?target=\"[a-zA-Z_0-9]*", "")
                        .replaceFirst("\"\\s*.*", "");
                if (valid(link)) {
                    links.add(link);
                }
            }
        } catch (IllegalStateException e) {
            e.printStackTrace();
        }
        return links;
    }

    private boolean valid(String s) {
        if (s.matches("javascript:.*|mailto:.*")) {
            return false;
        }
        return true;
    }

    private String makeAbsolute(String url, String link) {
        if (link.matches("http://.*")) {
            return link;
        }
        if (link.matches("/.*") && url.matches(".*$[^/]")) {
            return url + "/" + link;
        }
        if (link.matches("[^/].*") && url.matches(".*[^/]")) {
            return url + "/" + link;
        }
        if (link.matches("/.*") && url.matches(".*[/]")) {
            return url + link;
        }
        if (link.matches("/.*") && url.matches(".*[^/]")) {
            return url + link;
        }
        throw new RuntimeException("Cannot make the link absolute. Url: " + url
                + " Link " + link);
    }
}
  
}
