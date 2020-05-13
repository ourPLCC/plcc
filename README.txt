Note: Python3 and the Java SDK (version 5 or greater) must be installed
on your Linux platform.

WINDOWS: Before using the scripts described below, create a PLCC
directory somewhere in your Linux filesystem (such as your home directory)
and copy these scripts from THIS directory into your PLCC directory. Then
add the execute 'x' permission to the copied files. (This VFAT partition
does not support execute permissions, so you will not be able to execute
them directly unless you copy them.) Then add the entire path name of
your newly created PLCC directory to your PATH environment variable,
and create an environment variable LIBPLCC to point to the absolute path
of THIS folder name.

LINUX: Before running these files, set up the LIBPLCC environment
variable to point to the absolute path of THIS folder name and add THIS
folder name to your PATH environment variable.

ALL: If the environment variable is giving you trouble when running the Python
plcc.py file, you may need to change line 69 of the plcc.py Python file
to return the absolute path name of THIS folder.

You will also need java, javac, and python3 to be in your PATH environment
variable, should they not have been set by their installers. Make sure that
the python executable runs Python3, not Python2.

Here's a summary of the script files:

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


DOCKER: Experimental

Docker provides an alternate way to install and run PLCC. The
following command will run a bash terminal inside a docker container that
already has PLCC and its dependencies installed, and your current working
directory will be available inside the container so you can work on your files.

    docker run -it --rm -v ${PWD}:/home/guest ourPLCC/plcc

When you are done, type exit.
