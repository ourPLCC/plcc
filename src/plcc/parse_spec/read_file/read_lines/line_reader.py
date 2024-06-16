from pathlib import Path


from .line import Line


class LineReader:
    def read(self, file):
        file = Path(file)
        with file.open('r') as f:
            string = f.read()
        p = str(file.resolve())
        return [Line(string=s,number=k,file=p) for k, s in enumerate(string.splitlines(), start=1)]

