from importlib.resource import files


class Lexer():
    def __init__(self):
        self._termSpecs = None
        self._destinationDirectory = None

    def setTermSpecifications(self, termSpecs):
        self._termSpecs = termSpecs

    def setDestinationDirectory(self, d):
        self._destinationDirectory = Path(d)

    def generate(self):
        self._ensureDestinationDirectoryExists()
        self._copyFiles()
        self._createTokenFile()

    def _ensureDestinationDirectoryExists(self):
        self._destinationDirectory.mkdir(parents=True, exist_ok=True)

    def _copyFiles(self):
        for file in files('.lib'):
            if file.is_file():
                f = file.as_file()
                try:
                    shutil.copy(f, self._destinationDirectory / f.name)
                except:
                    d = str(self._destinationDirectory)
                    raise Exception(f'Failure copying {f} to {d}')

    def _createTokenFile(self):
        self._builder.getTokenFile().write(self._destinationDirectory)

    def _getFilesNamesToCopy(self):
        return [f'{c}.java' for c in self._classesToCopyFromStd]

    def _getTokenFile(self):
        return TokenFileBuilder().buildTokenFile(self._termSpecs)
