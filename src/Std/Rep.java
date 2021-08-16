import java.io.*;
import java.util.*;

public class Rep extends ProcessFiles {

    // Parse the program and call $run() on the resulting parse tree
    public void action(Scan scn, Trace trace) {
        _Start.parse(scn, trace).$run();
    }

    // Run programs from command-line files
    // and then perform a read-eval-print loop on programs
    // read from standard input.
    public static void main(String [] args) {
        new Rep().processFiles(args);
    }
}
