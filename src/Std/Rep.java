import java.io.*;
import java.util.*;

public class Rep {

    // Run programs from command-line files
    // and then perform a read-eval-print loop on programs
    // read from standard input.
    // Parse each program and evaluate $run() on the resulting parse tree
    public static void main(String [] args) {
        ProcessFiles.main(args, false);
    }
}
