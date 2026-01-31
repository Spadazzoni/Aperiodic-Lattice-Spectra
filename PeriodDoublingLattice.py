import numpy as np
from scipy.linalg import eigh_tridiagonal


def NewPeriodDoubling(Seed, NumberOfSubstitutions):
    Lattice = []
    NewList = []
    if len(Seed.split(",")) == 1:
        for i in range(NumberOfSubstitutions):
            if i == 0:
                if Seed == "0":
                    Lattice.extend([0, 1])
                if Seed == "1":
                    Lattice.extend([0, 0])
            if i > 0:
                for item in Lattice:
                    if item == 0:
                        NewList.extend([0, 1])
                    if item == 1:
                        NewList.extend([0, 0])
                Lattice = NewList
                NewList = []
    elif len(Seed.split(",")) == 2:
        LeftLattice = NewPeriodDoubling(Seed.split(",")[0], NumberOfSubstitutions)
        ShortenedLeftLattice = LeftLattice[int(0.9 * len(LeftLattice)) :]
        RightLattice = NewPeriodDoubling(Seed.split(",")[1], NumberOfSubstitutions)
        Lattice = ShortenedLeftLattice + RightLattice
    return Lattice


def Potential(Seed, NumberOfSubstitutions, TimeSteps):
    Lattice = NewPeriodDoubling(Seed, NumberOfSubstitutions)
    Lenght = len(Lattice)
    Pot = []
    FullPotential = []
    for i in range(0, Lenght):
        if Lattice[i] == 0:
            Pot.append(-1)
        if Lattice[i] == 1:
            Pot.append(1)
        if i > 0:
            for TimeTick in range(TimeSteps):
                FullPotential.append(
                    Pot[i - 1] * (1 - TimeTick / TimeSteps)
                    + Pot[i] * TimeTick / TimeSteps
                )
    return FullPotential


def Hamiltonian(Size, Mass, Seed, NumberOfSubstitutions, TimeSteps, TimeIndex):
    Pot = Potential(Seed, NumberOfSubstitutions, TimeSteps)
    Diagonal = np.zeros(Size)
    OffDiagonal = Mass * np.ones(Size - 1)
    for i in range(Size):
        Diagonal[i] = Pot[TimeIndex + i * TimeSteps]
    return Diagonal, OffDiagonal


def DivideFullSpectrum(
    Iteration,
    FullSpectrum,
    LeftSpectrum,
    RightSpectrum,
    EigenVectors,
    LeftIndex,
    RightIndex,
    TimeIndex,
    Size,
    TimeSteps,
    BoundaryLenght,
    DecisionFactor,
):
    for i in range(Size):
        iThEigenVector = EigenVectors[:, i]
        LeftIntegral = np.sum(
            np.abs(iThEigenVector[0 : int(Size * BoundaryLenght)]) ** 4
        )
        RightIntegral = np.sum(
            np.abs(iThEigenVector[Size - int(Size * BoundaryLenght) : Size]) ** 4
        )
        CenterIntegral = (
            np.sum(np.abs(iThEigenVector) ** 4) - LeftIntegral - RightIntegral
        )
        if LeftIntegral > DecisionFactor * (CenterIntegral + RightIntegral):
            LeftSpectrum.append(FullSpectrum[TimeIndex, i])
            LeftIndex.append(Iteration / TimeSteps)
            FullSpectrum[TimeIndex, i] = np.nan
        elif RightIntegral > DecisionFactor * (CenterIntegral + LeftIntegral):
            RightSpectrum.append(FullSpectrum[TimeIndex, i])
            RightIndex.append(Iteration / TimeSteps)
            FullSpectrum[TimeIndex, i] = np.nan
    return FullSpectrum, LeftSpectrum, LeftIndex, RightSpectrum, RightIndex


def FibonacciSpectrum(
    TotalTimeTranslations,
    TimeSteps,
    Size,
    Seed,
    NumberOfSubstitutions,
    BoundaryLenght,
    DecisionFactor,
    Mass,
):
    LeftSpectrum = []
    LeftIndex = []
    RightSpectrum = []
    RightIndex = []
    FullSpectrum = np.zeros((TimeSteps * TotalTimeTranslations, Size))
    for Translation in range(TotalTimeTranslations):
        for TimeTick in range(TimeSteps):
            TimeIndex = Translation * TimeSteps + TimeTick
            Diagonal, OffDiagonal = Hamiltonian(
                Size, Mass, Seed, NumberOfSubstitutions, TimeSteps, TimeIndex
            )
            FullSpectrum[TimeIndex, :], EigenVectors = eigh_tridiagonal(
                Diagonal, OffDiagonal
            )
            FullSpectrum, LeftSpectrum, LeftIndex, RightSpectrum, RightIndex = (
                DivideFullSpectrum(
                    TimeIndex,
                    FullSpectrum,
                    LeftSpectrum,
                    RightSpectrum,
                    EigenVectors,
                    LeftIndex,
                    RightIndex,
                    TimeIndex,
                    Size,
                    TimeSteps,
                    BoundaryLenght,
                    DecisionFactor,
                )
            )
    return FullSpectrum, LeftSpectrum, LeftIndex, RightSpectrum, RightIndex


def FullSpectrum(Size, Mass, Seed, NumberOfSubstitutions, TimeSteps, TotalTranslations):
    TotalSteps = TimeSteps * TotalTranslations
    FullSpectrum = np.zeros((TotalSteps, Size))
    for Translation in range(TotalTranslations):
        for TimeTick in range(TimeSteps):
            TimeIndex = Translation * TimeSteps + TimeTick
            Diagonal, OffDiagonal = Hamiltonian(
                Size, Mass, Seed, NumberOfSubstitutions, TimeSteps, TimeIndex
            )
            FullSpectrum[TimeIndex, :] = eigh_tridiagonal(Diagonal, OffDiagonal, True)
    return FullSpectrum
