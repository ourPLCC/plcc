// WIP File

import java.util.*;
import java.io.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

public class ParseJsonAst extends ProcessFiles {

    // Parse the program and call $ok() on the resulting parse tree
    public void action(Scan scn, Trace trace) {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.disable(SerializationFeature.FAIL_ON_EMPTY_BEANS);
        _Start parseTree = _Start.parse(scn, trace);
        parseTree.$ok();
        try {
            objectMapper.writeValue(new File("AST.json"), parseTree);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Read programs from command-line files
    // and then read programs from standard input.
    public static void main(String [] args) {
        new ParseJsonAst().processFiles(args);
    }
}
