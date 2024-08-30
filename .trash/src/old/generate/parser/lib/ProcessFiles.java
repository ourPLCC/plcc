import java.io.*;
import java.util.*;

// Process command-line arguments (flags, filenames) from the given args
// Read programs from named files and then from standard input.
// If the '-n' flag is given, don't prompt for standard input,
//     otherwise prompt with "--> "
// If the '-t' command line argument is given, toggle the trace feature
//     (defaults to no trace)
// For each input program, use 'action' to parse the input
//     and act on the resulting parse tree

public abstract class ProcessFiles {

    // build a parse tree and act on it
    abstract void action(Scan scn, Trace trace);

    public void processFile(Scan scn, Trace trace, String prompt, String prog) {
        try {
            // read and process programs from this 
            while(true) {
                System.out.print(prompt);
                if (scn.isEOF())
                    break;
                if (trace != null)
                    trace.reset();
                if (prog != null) {
                    System.out.print(prog);
                    if (trace != null)
                        System.out.println(); // format the trace better
                }
                action(scn, trace);
            }
        } catch (Exception e) {
            System.err.println(e.getMessage());
        } catch (Error e) {
            System.err.println(e);
            System.exit(1);
        }
    }

    public void processFiles(String [] args) {
        Trace trace = null;
        // first read and process any input files from the command line
        Scan scn = null;
        String prog = null;
        String prompt = "--> ";
        for (int i=0 ; i<args.length ; i++) {
            String s = args[i];
            if (s.equals("-n")) {
                // turns off prompts when reading from stdin
                prompt = "";
                continue;
            }
            if (s.equals("-t")) {
                // toggle traces
                trace = (trace == null ? new Trace() : null);
                continue;
            }
            if (s.equals("-v")) {
                // toggle verbose cmd line name output
                prog = (prog == null ? "" : null);
                continue;
            }
            try {
                scn = new Scan(new BufferedReader(new FileReader(s)));
            } catch (FileNotFoundException e) {
                System.err.println(s + ": no such file ... exiting");
                System.exit(1);
            }
            if (prog != null)
                prog = "[" + s + "]";
            processFile(scn, trace, "", prog);
        }
        // finally read and process programs from standard input
        BufferedReader rdr =
            new BufferedReader(new InputStreamReader(System.in));
        scn = new Scan(rdr);
        if (prog != null)
            prog = "[stdin]";
        processFile(scn, trace, prompt, prog);
    }

}
