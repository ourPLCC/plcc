from dataclasses import dataclass


@dataclass
class File:
    name: str
    contents: str

    def write(self, destDir):
        path = destDir / self.name
        with path.open('w') as outFile:
            print(self.contents, file=outFile)
