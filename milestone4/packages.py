""" Helper module for the package installability problem"""

import gzip


class Package:
    """An installable package.

    Members:
    index -- index in the repository
    name -- the name of the package
    depends -- list of tuples representing the dependencies, each tuple is a
        disjunction of package names
    conflicts -- set of package names that conflict with this package
    provides -- set of package names this package provides
    provided_by -- set of package names of packages providing this package

    """

    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.depends = []
        self.conflicts = set()
        self.provides = set()
        self.provided_by = set()

    def __repr__(self):
        return "<Package {}>".format(self.name)

    def __str__(self):
        return self.name


class Repository:
    """A repository is a collection of packages. Packages are indexed starting
    from 1."""
    
    def __init__(self, filename):
        """Load a gzipped package list."""
        self.packages = []
        self.map = {}

        def getpkg(name):
            if name not in self.map:
                pkg = Package(len(self.packages) + 1, name)
                self.packages.append(pkg)
                self.map[name] = pkg
            return self.map[name]

        with gzip.open(filename) as f:
            current = None
            for line in f:
                line = line.decode().strip()
                if not line:
                    continue
                cmd = line[:line.index(":")]
                args = line[line.index(":") + 1:]
                if cmd == "Package":
                    current = getpkg(args.strip())
                elif cmd == "Depends":
                    for d in args.split(","):
                        current.depends.append(tuple(getpkg(p.strip())
                                                     for p in d.split("|")))
                elif cmd == "Conflicts":
                    current.conflicts = set(getpkg(p.strip())
                                            for p in args.split(","))
                elif cmd == "Provides":
                    current.provides = set(getpkg(p.strip())
                                           for p in args.split(","))
                    for p in current.provides:
                        p.provided_by.add(current)

    def __len__(self):
        return len(self.packages)

    def __contains__(self, x):
        if isinstance(x, Package):
            x = x.name
        return x in self.map

    def __getitem__(self, x):
        if isinstance(x, int):
            return self.packages[x - 1]
        else:
            return self.map[x]

    def __iter__(self):
        return iter(self.packages)
