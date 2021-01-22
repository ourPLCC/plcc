import java.util.regex.*;
import java.util.*;
import java.io.*;

public class Scan implements IScan {

    private BufferedReader rdr;  // get input from here, line by line
    private String s;            // current string being scanned
    private int start;           // starting position in the string to scan
    private int end;             // ending position

    public int lno;              // current line number
    public Token tok;            // this is persistent across all calls to cur()

    // create a scanner object on a buffered reader
    public Scan(BufferedReader rdr) {
        this.rdr = rdr;
        this.lno = 0;
        s = null;
        tok = null;
    }

    // create a scanner object on a string
    public Scan(String s) {
        this(new BufferedReader(new StringReader(s)));
    }

    public void reset() {
        // force the scanner to process the next line
        s = null;
        tok = null;
    }

    // fill the string buffer from the reader if it's exhausted or null)
    public void fillString() {
        if (s == null || start >= end) {
            // get the next line from the reader
            try {
                s = rdr.readLine();
                if (s == null)
                    return; // end of file
                lno++;
                s += "\n";
                start = 0;
                end = s.length();
            } catch (IOException e) {
                s = null;
            }
            // System.err.print("s=" + s);
        }
    }
        
    public Token cur() {
        // lazy
        if (tok != null)
            return tok; // don't get a new token if we already have one

        String matchString = "";
        Token.Val valFound = null;

        LOOP:
        while (true) {
            fillString(); // get another line if necessary
            if (s == null) {
                tok = new Token(Token.Val.$EOF, "!EOF", lno); // EOF
                return tok;
            }
            // s cannot be null here
            int matchEnd = start; // current end of match
            for (Token.Val val : Token.Val.values()) {
                Pattern pat = val.cPattern;
                if (pat == null)
                    break; // nothing matches, so can't find a token
                if (val.skip && valFound != null)
                    continue; // ignore skips if we have a pending token
                Matcher m = pat.matcher(s);
                m.region(start, end);
                if (m.lookingAt()) {
                    int e = m.end();
                    if (e == start)
                        continue; // empty match, so try next pattern
                    if (val.skip) {
                        // there's a non-empty skip match,
                        // so we skip over the matched part
                        // and get more stuff to read
                        start = e;
                        continue LOOP;
                    }
                    if (matchEnd < e) {
                        // found a longer match -- keep it!
                        matchEnd = e;
                        matchString = m.group();
                        valFound = val;
                    }
                }
            }
            if (valFound == null) { // got to $ERROR, so nothing matches!!
                char ch = s.charAt(start++); // grab the char and advance
                String sch;
                if (ch >= ' ' && ch <= '~')
                    sch = String.format("\"%c\"", ch);
                else
                    sch = String.format("\\u%04x", (int)ch);
                tok = new Token(Token.Val.$ERROR, "!ERROR("+sch+")", lno);
                return tok;
            }
            start = matchEnd; // start of next token match
            // matchString is the matching string
            tok = new Token(valFound, matchString, lno); // persistent value
            return tok;
        }
    }

    public void adv() {
        // if we have already advanced past the current token,
        // we'll have to do it again
        if (tok == null)
            cur();
        tok = null;
    }

    public void put(Token t) {
            throw new RuntimeException("\n>>> Scan class: put not implemented");
    }

    public Token match(Token.Val v, Trace trace) {
        Token t = cur();
        Token.Val vv = t.val;
        if (v == vv) {
            if (trace != null)
                trace.print(t);
            adv();
        } else {
            String str;
            if (vv == Token.Val.$ERROR)
                str = t.toString();
            else
                str = vv.toString();
            throw new RuntimeException
                ("\n>>> match failure: expected token " + v + ", got " + str);
        }
        return t;
    }

    public boolean isEOF() {
        return cur().isEOF();
    }

    public void printTokens() {
        while (hasNext()) {
            Token t = next();
            String s;
            switch(t.val) {
            case $ERROR:
                s = t.str;
                break;
            default:
                s = String.format("%s '%s'", t.val.toString(), t.str);
            }
            System.out.println(String.format("%4d: %s", lno, s));
        }
    }

    public boolean hasNext() {
        return !cur().isEOF();
    }

    public Token next() {
        Token t = cur();
        adv();
        return t;
    }

    public static void main(String [] args) {
        BufferedReader rdr =
            new BufferedReader(new InputStreamReader(System.in));
        Scan scn = new Scan(rdr);
        scn.printTokens();
    }
}
