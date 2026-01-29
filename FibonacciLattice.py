import numpy as np


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


def Potential(Seed, NumberOfSubstitutions, TimeSteps):
    Lattice = NewFibonacci(Seed, NumberOfSubstitutions)
    Lenght = len(Lattice)
    Potential = []
    FullPotential = []
    for i in range(1, Lenght):
        if Lattice[i] == 0:
            Potential.append(-1)
        if Lattice[i] == 1:
            Potential.append(1)
        for TimeTick in range(TimeSteps):
            FullPotential.append(
                Potential[i] * (1 - TimeTick / TimeSteps)
                + Potential[i - 1] * TimeTick / TimeSteps
            )
    return FullPotential


def Hamiltonian(Size, Mass, Seed, NumberOfSubstitutions, TimeSteps, TimeIndex):
    Potential = Potential(Seed, NumberOfSubstitutions, TimeSteps)
    Diagonal = np.zeros(Size)
    OffDiagonal = Mass * np.ones(Size-1)
    for i in range(Size):
        Diagonal[i] = Potential[TimeIndex + i * TimeSteps]
    return Diagonal, OffDiagonal


