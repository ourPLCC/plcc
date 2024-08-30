import java.util.*;
import java.io.*;


public class Parse extends ProcessFiles {

    // Parse the program and call $ok() on the resulting parse tree
    public void action(Scan scn, Trace trace) {
        _Start.parse(scn, trace).$ok();
    }

    // Read programs from command-line files
    // and then read programs from standard input.
    public static void main(String [] args) {
        new Parse().processFiles(args);
    }
}
