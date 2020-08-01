import java.util.*;
import java.io.*;

// parses the strings given on the command line
// and prints their results
public class Parser {

    public Scan scn; // scanner object

    public Parser(BufferedReader rdr) {
        scn = new Scan(rdr);
    }

    public static void parse(Scan scn, Trace trace) {
        try {
            System.out.println(PLCC$Start.parse(scn, trace));
            // System.out.println("OK");
        } catch (NullPointerException e) {
            System.out.println("Premature end of input");
        } catch (Exception e) {
            System.out.println(e);
        } 
    }

    public static void main(String [] args) {
	Trace trace = null;
        int start = 0;
        if (args.length > 0 && args[0].equals("-t")) {
            trace = new Trace();
            System.out.println("tracing ...");
            start++;
        }
        if (start == args.length) {
            BufferedReader rdr =
                new BufferedReader(new InputStreamReader(System.in));
            Scan scn = new Scan(rdr);
            parse(scn, trace);
            return;
        }
        for (int i=start ; i<args.length ; i++) {
            String s = args[i];
            Scan scn = new Scan(new BufferedReader(new StringReader(s)));
            if (trace != null) {
	        trace.reset();
                System.out.println();
            }
            System.out.print(s + " -> ");
            parse(scn, trace);
        }
    }
}
