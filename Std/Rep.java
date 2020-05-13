import java.io.*;
import java.util.*;

public class Rep {

    // do a read-eval-print loop, reading from command-line files
    // and then from standard input
    public static void main(String [] args) {
	Trace trace = null;
	// first read and process any input files from the command line
	Scan scn = null;
        String prompt = "--> ";
	for (int i=0 ; i<args.length ; i++) {
	    String s = args[i];
            if (s.equals("-n")) {
                prompt = "";
                continue;
            }
            if (s.equals("-t") && trace == null) {
                trace = new Trace(); // trace any following args
                continue;
            }
	    try {
		scn = new Scan(new BufferedReader(new FileReader(s)));
            } catch (FileNotFoundException e) {
		System.out.println(s + ": no such file ... exiting");
                System.exit(1);
            }
	    try {
		// read and process expressions from this FileReader
		while (true) {
		    if (trace != null)
			trace.reset();
                    if (scn.isEOF())
                        break;
		    System.out.println(PLCC$Start.parse(scn, trace));
                }
            } catch (Exception e) {
		System.out.println(e.getMessage());
            } catch (Error e) {
		System.out.println(e.getMessage());
                System.exit(1);
            }
           
        }
        // finally read any expressions from standard input
	BufferedReader rdr =
            new BufferedReader(new InputStreamReader(System.in));
        scn = new Scan(rdr);
        while (true) {
            System.out.print(prompt);
            try {
                if (scn.isEOF()) {
                    System.out.println();
                    break; // all done!
                }
		if (trace != null) {
		    trace.reset();
                    System.out.println(); // format the trace better
                }
                System.out.println(PLCC$Start.parse(scn, trace)); // parse and print
            } catch (Exception e) {
                System.out.println(e.getMessage());
                scn.reset(); // start over with a new  line
            } catch (Error e) {
                System.out.println(e.getMessage());
                System.exit(1);
            }
        }
    }
}
