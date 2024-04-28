public interface ITrace {

    public void print(Token t);

    public void print(String s, int lno);

    public Trace nonterm(String s, int lno);

    public void reset();

}
