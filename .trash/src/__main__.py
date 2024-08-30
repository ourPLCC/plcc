# -*-python-*-

"""
    PLCC: A Programming Languages Compiler-Compiler
    Copyright (C) 2023  Timothy Fossum <plcc@pithon.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import re
import os
import pathlib
import io
import shutil
import tempfile

import plcc.version
from plcc.parse.specreader import SpecificationReader

from plcc.stubs.java import JavaStubs
from plcc.stubs.python import PythonStubs
from plcc.stubs.stubs import StubDoesNotExistForHookException

from plcc.specification_file import SpecificationParser


# current file information
Fname = ''          # current file name (STDIN if standard input)
Lno = 0             # current line number in file
Line = ''           # current line in the file
nlgen = None        # next line generator for Fname
STD = []            # reserved names from Std library classes
STDT = []           # token-related files in the Std library directory
STDP = []           # parse/runtime-related files in the Std library directory

flags = {}          # processing flags (dictionary)

lineMode = False    # True if in line mode

startSymbol = ''    # start symbol (first nonterm in rules)
term = set()        # set of term (token) names
termSpecs = []      # term (token) specifications for generating the Token file

nonterms = set()    # set of all nonterms
fields = {}         # maps a non-abstract class name to its list of fields
rules = []          # list of items  of the form (nt, cls, rhs),
                    # one for each grammar rule
extends = {}        # maps a derived class to its abstract base class
derives = {}        # maps an abstract class to a list of its derived classes
cases = {}          # maps a non-abstract class to its set of case terminals
                    # for use in a switch
rrule = {}          # maps a repeating rule class name to its separator string
                    # (or None)

def debug(msg, level=1):
    # print(getFlag('debug'))
    if msg and getFlag('debug') >= level:
        print('%%% {}'.format(msg), file=sys.stderr)
        return True
    return False

def debug2(msg):
    debug(msg, level=2)

def LIBPLCC():
    return str(pathlib.Path(__file__).parent)


class Main():
    def __init__(self):
        self._STDT = ['ILazy','IMatch','IScan','ITrace', 'Trace', 'PLCCException', 'Scan']
        self._STDP = ['ProcessFiles','Parse','Rep','ParseJsonAst']
        self._STD = self._STDT + self._STDP
        self._STD.append('Token')
        self._flags = self._getDefaultFlags()
        self._specificationFilePath = None

    def _getDefaultFlags(self):
        # file-related flags -- can be overwritten
        # by a grammar file '!flag=...' spec
        # or by a '--flag=...' command line argument
        flags = {}
        for fname in self._STD:
            flags[fname] = fname
        flags['libplcc'] = LIBPLCC()
        flags['Token'] = True         # generate scanner-related files
        # behavior-related flags
        flags['debug'] = 0                  # default debug value
        flags['destdir'] = 'Java'           # the default destination directory
        flags['python_destdir'] = 'Python'  # default destination for fourth section semantics (Python)
        flags['pattern'] = True             # create a scanner that uses re. patterns
        flags['LL1'] = True                 # check for LL(1)
        flags['parser'] = True              # create a parser
        flags['semantics'] = True           # create java semantics routines
        flags['python_semantics'] = True    # create python semantics routines
        flags['nowrite'] = False            # when True, produce *no* file output
        flags['version'] = False            # when True, print the version and exit.
        return flags

    def main(self, argv):
        try:
            self._processCommandLine(argv)
            if self._flags['version']:
                self._printVersion()
            else:
                self._loadSpecification()
                self._generateLanguageSystem()
        except ParseException as e:
            self._handleParseException(e)
        except Exception as e:
            self._handleException(e)

    def _processCommandLine(self, argv):
        cl = CommandLineProcessor()
        cl.process(argv)
        fs = cl.getFlags()
        self._flags.update(fs)
        self._specificationFilePath = cl.getSpecificationFilePath()

    def _printVersion(self):
        print(plcc.version.get_version())

    def _loadSpecification(self):
        plcc.spec.load.Loader().load(self._specificationFilePath)

    def _generateLanguageSystem(self):
        builder = Builder()
        builder.build(self._specification)

        if self._flags['nowrite']:
            return
        if not self._flags['Token']:
            return # do not create any automatically generated scanner-related files

        generator.generate(builder)


    def _orphans_from_old_main():
        java = JavaStubs()
        python = PythonStubs()
        par(nxt, java, python)    # LL(1) check and parser generation
        sem(nxt, java, destFlag='destdir', semFlag='semantics', fileExt='.java')
        sem(nxt, python, destFlag='python_destdir', semFlag='python_semantics', fileExt='.py')
        done()

    def _handleParseException(self, exception):
        m = f'{self._line.line:4} [{self._line.file}]: {self._message}\nline: {self._line.text}'
        print(m, file=sys.stderr)
        sys.exit(1)

    def _handleException(self, exception):
        print(str(exception), file=sys.stderr)
        sys.exit(1)


#####################
# utility functions #
#####################

def getFlag(s):
    global flags
    if s in flags:
        return flags[s]
    else:
        return None


def push(struct, item):
    struct.append(item)


class CommandLineProcessor():
    def __init__(self):
        self._flags = {}
        self._specificationFilePath = None

    def process(self, argv):
        argv = argv.copy()
        argv = self._processFlagArguments(argv)
        argv = self._processPositionalArguments(argv)
        if argv:
            raise Exception('Additional unknown positional arguments given: "{' '.join(argv)}"')

    def _processFlagArguments(self, argv):
        argv = argv.copy()
        while argv:
            if self._argv[0] == '--':
                # just continue with the rest of the command line
                argv = argv[1:]
                break
            (flag, ee, val) = argv[0].partition("=")
            flag = flag.strip()
            if  flag[:2] == '--':
                key = flag[2:].strip()
                if key == '':
                    raise Exception('illegal command line parameter')
                val = val.strip()
                if ee:
                    self._processFlag(f'{key}={val}')
                else:
                    self._processFlag(key)
                argv = argv[1:]
            else:
                break
        if not argv:
            raise Exception('No specification file given.')
        return argv

    def _processFlag(self, flagSpec):
        # flagSpec has been stripped
        (key,ee,val) = flagSpec.partition('=')
        key = key.rstrip()
        if re.match(r'[a-zA-Z]\w*$', key) == None:
            raise Exception('malformed flag specification: !' + flagSpec)
        val = val.lstrip()
        # '!key' makes key true, whereas '!key=' makes key false
        if ee == '':     # missing '='
            val = True
        elif val == '':  # empty val
            val = False
        # treat the debug flag specially
        if key == 'debug':
            if val == False:
                val = 0
            elif val == True:
                val = 1
            else:
                try:
                    val = int(val)
                    if val < 0:
                        val = 0
                except:
                    raise Exception('improper debug flag value')
        self._flags[key] = val

    def _processPositionalArguments(argv):
        if not argv:
            raise Exception('No specification file given.')
        self._specificationFile = argv[0]
        argv = argv[1:]
        return argv

    def getFlags(self):
        return self._flags.copy()

    def getSpecificationFilePath(self):
        return self._specificationFilePath


if __name__ == '__main__':
    main()
