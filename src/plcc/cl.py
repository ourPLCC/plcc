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

