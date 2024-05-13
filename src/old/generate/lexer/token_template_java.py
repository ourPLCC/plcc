from .file import File


class TokenTemplateJava(File):
    def __init__(self):
        super().__init__('Token.java')
        self._termSpecs = None

    def setTerminalSpecifications(self, termSpecs):
        self._termSpecs = termSpecs

    def buildContents(self):
        enumDeclarations = self._buildEnumDeclarations(termSpecs)
        self.contents =  f'''\
import java.util.*;

// bare Token class for use with hand-crafted scanners
public class Token {{

    public enum Match {{
{enumDeclarations}
    }}

    public Match match;      // token match
    public String str;       // this token's lexeme (never empty!)
    // the following two fields may be unused
    public int lno;          // the line number where this token was found
    public String line;      // the text line where this token appears

    public Token() {{
        match = null;
        str = null;
        lno = 0;
        line = null;
    }}

    public Token(Match match, String str, int lno, String line) {{
        this.match = match;
        this.str = str;
        this.lno = lno;
        this.line = line;
    }}

    public Token(Match match, String str) {{
        this(match, str, 0, null);
    }}

    public String toString() {{
        return str;
    }}

    public static void main(String [] args) {{
        for (Match match: Match.values()) {{
            System.out.println( String.format("%s", match));
        }}
    }}

//Token//

}}
'''

    def _buildEnumDeclarations(self, termSpecs):
        lineSeparator = ',\n'
        endPunctuation = ''
        lines = [f'{ts}' for ts in termSpecs]
        lines = indentLines(2, lines)
        string = lineSeparator.join(lines)
        string += endPunctuation()
        return string
