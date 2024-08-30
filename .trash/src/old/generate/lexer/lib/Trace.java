import java.io.*;

public class Trace implements ITrace {

    public String indent;
    public PrintStream out;

    public Trace(PrintStream out, String indent) {
        this.out = out;
        this.indent = indent;
    }

    public Trace(PrintStream out) {
        this(out, "");
    }

    public Trace() {
        this(System.err); // output defaults to System.err
    }

    public void print(String s, int lno) {
        if (out != null)
            out.printf("%4d: %s\n", lno, indent + s);
    }

    public void print(Token t) {
        print(t.match.toString()+" \""+t.toString()+"\"", t.lno);
    }

    public Trace nonterm(String s, int lno) {
        print(s, lno);
        return new Trace(out, indent + "| ");
    }

    public void reset() {
        indent = "";
    }

}
