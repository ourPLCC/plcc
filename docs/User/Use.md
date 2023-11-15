Whether you are running inside of Docker, a terminal running a Bash shell, a PowerShell, or a Windows command prompt, the commands should be the same.

Here's a summary of the PLCC commands:

```
plcc                    runs plcc.py on 'file'
plccmk [-c] [file]:     runs plcc.py on 'file' and uses javac to compile all
                            of the resulting Java files in the Java directory.
                        The optional '-c' flag will remove all previous
                            Java files if there were any
                        The 'file' name defaults to 'grammar'
scan:                   Runs the Java/Scan program (only scan for tokens)
parse:                  Runs the Java/Parser program (only scan and parse)
rep:                    Runs the Java/Rep program
                            (scan, parse, and enter read-eval-print loop)
rep-t:                  Runs the Java/Rep program with the trace flag
```