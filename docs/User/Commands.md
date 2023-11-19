# Commands

## Quick reference

```
plcc file
                        runs plcc.py on 'file', which generates
                            code in a directory named 'Java/'.
plccmk [-c] [file]
                        runs plcc.py on file and compiles its results.
                        '-c' Remove 'Java/' before regenerating it.
                        'file' defaults to 'grammar'
scan [file...]
                        Run Java/Scan on each file and then stdin.
                            Scans input printing recognized token.
parse [-t] [-n] [file...]
                        Run Java/Parser on each file and then stdin.
                            Scans and parses input, printing OK for recognized
                            programs and error otherwise.
                        '-t' Print trace (i.e., parse tree).
                        '-n' Suppress prompt.
rep [-t] [-n] [file...]
                        Run Java/Rep on each file and then stdin.
                            REP = Read, Execute, and Print loop.
                            Scans, parses, and evaluates each program
                            in the input.
                        '-t' Print trace (i.e., parse tree).
                        '-n' Suppress prompt.
```
