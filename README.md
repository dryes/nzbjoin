nzbjoin
=====

nzbjoin takes multiple nzb input files and merges them together, properly.

## dependencies:
* Python2
* [pynzb][pynzb]

## usage:
* nzbjoin.py [--opts] file1.nzb file2.nzb ...

## notes:
* default behaviour is to overwrite first nzb file passed with contents of all.
* to output to specific file use: -o path/to/output/file.nzb
* to delete input files: -d

[pynzb]: https://pypi.python.org/pypi/pynzb/
