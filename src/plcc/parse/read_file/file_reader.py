from .include_files import IncludeReader


class FileReader:
    def read(self, file):
        return IncludeReader().read(file)
