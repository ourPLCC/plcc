import java.util.*;
import java.io.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.databind.jsontype.PolymorphicTypeValidator;
import com.fasterxml.jackson.databind.jsontype.BasicPolymorphicTypeValidator;



public class ParseJsonAst extends ProcessFiles {

    // Parse the program and call $ok() on the resulting parse tree
    public void action(Scan scn, Trace trace) {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.disable(SerializationFeature.FAIL_ON_EMPTY_BEANS);
        objectMapper.enable(SerializationFeature.WRAP_ROOT_VALUE);
        objectMapper.enable(SerializationFeature.INDENT_OUTPUT);

        PolymorphicTypeValidator ptv = BasicPolymorphicTypeValidator
        .builder()
        .allowIfBaseType(Object.class) // Can change "Object" to any type, we can look back at this later to be more specific
        .build();

        objectMapper.activateDefaultTypingAsProperty(ptv, ObjectMapper.DefaultTyping.NON_FINAL, "$type");

        _Start parseTree = _Start.parse(scn, trace);
        parseTree.$ok();
        try {
            objectMapper.writeValue(new File("JsonAST.json"), parseTree);
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
