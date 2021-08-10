import java.io.*;
import java.util.*;

// Process command-line arguments (flags, filenames) from the given args
// Read programs from named files and then from standard input.
// If the '-n' flag is given, don't prompt for standard input,
//     otherwise prompt with "--> "
// If the '-t' command line argument is given, toggle the trace feature
//     (defaults to no trace)
// For each input program, parse the input to get a parse tree.
//     If parseOnly is true, apply the $ok() method on the parse tree
//         (defaults to printing "OK")
//     If parseOnly is false, apply the $run() method on the parse tree
//         (defaults to printing the toString representation of
//          the root of the parse tree)
public class ProcessFiles {

    private static void run(Scan scn, Trace trace, boolean parseOnly) {
        _Start parseTree = _Start.parse(scn, trace);
        if (parseOnly) {
            parseTree.$ok();
        } else {
            parseTree.$run();
        }
    }

    public static void main(String [] args, boolean parseOnly) {
        Trace trace = null;
        // first read and process any input files from the command line
        Scan scn = null;
        String prompt = "--> ";
        for (int i=0 ; i<args.length ; i++) {
            String s = args[i];
            if (s.equals("-n")) {
                prompt = "";             // turn off prompts
                continue;
            }
            if (s.equals("-t")) {
                if (trace == null) {
                    trace = new Trace(); // turn on tracing
                } else {
                    trace = null;        // turn off tracing
                }
                continue;
            }
            try {
                scn = new Scan(new BufferedReader(new FileReader(s)));
            } catch (FileNotFoundException e) {
                System.out.println(s + ": no such file ... exiting");
                System.exit(1);
            }
            try {
                // read and process programs from this FileReader
                while(true) {
                    if (scn.isEOF())
                        break;
                    if (trace != null)
                        trace.reset();
                    run(scn, trace, parseOnly);
                }
            } catch (Exception e) {
                System.out.println(e.getMessage());
            } catch (Error e) {
                System.out.println(e.getMessage());
                System.exit(1);
            }
        }
        // finally read and process programs from standard input
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
                run(scn, trace, parseOnly);
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
