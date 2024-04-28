public class PLCCException extends RuntimeException {

    String msg;

    public PLCCException(String pfx, String msg) {
        super(msg = "%%% " + pfx + ": " + msg);
        this.msg = msg;
    }

    public PLCCException(String msg) {
        this("Runtime error", msg);
    }

    public String toString() {
        return msg;
    }

}
