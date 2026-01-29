def NewFibonacci(Seed, NumberOfSubstitutions):
    Lattice = []
    NewList = []
    if len(Seed.split(",")) == 1:
        for i in range(NumberOfSubstitutions):
            if i == 0:
                if Seed == "0":
                    Lattice.extend([1, 0])
                if Seed == "1":
                    Lattice.append(0)
            if i > 0:
                for item in Lattice:
                    if item == 0:
                        NewList.extend([1, 0])
                    if item == 1:
                        NewList.append(0)
                Lattice = NewList
                NewList = []
    elif len(Seed.split(",")) == 2:
        LeftLattice = NewFibonacci(Seed.split(",")[0], NumberOfSubstitutions)
        ShortenedLeftLattice = LeftLattice[int(0.9 * len(LeftLattice)) :]
        RightLattice = NewFibonacci(Seed.split(",")[1], NumberOfSubstitutions)
        Lattice = ShortenedLeftLattice + RightLattice
    return Lattice
