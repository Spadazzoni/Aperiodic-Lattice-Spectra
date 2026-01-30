import PeriodDoublingLattice as fl
import matplotlib.pyplot as plt
import numpy as np
import timeit


def main():
    start = timeit.default_timer()
    NumberOfSubstitutions = 10  # 10
    TotalTimeTranslations = 50  # 50
    Size = 70  # 70
    TimeSteps = 100  # 100
    BoundaryLenght = 0.2  # 0.2
    DecisionFactor = 8  # 8
    TotalNumberOfSteps = TimeSteps * TotalTimeTranslations
    MassFactor = 1  # 1
    SeedPlus = "0,0"
    SeedMinus = "0,1"

    FullSpectrumPlus, LeftSpectrumPlus, LeftIndexPlus, RightSpectrumPlus, RightIndex = (
        fl.FibonacciSpectrum(
            TotalTimeTranslations,
            TimeSteps,
            Size,
            SeedPlus,
            NumberOfSubstitutions,
            BoundaryLenght,
            DecisionFactor,
            MassFactor,
        )
    )
    (
        FullSpectrumMinus,
        LeftSpectrumMinus,
        LeftIndexMinus,
        RightSpectrumMinus,
        RightIndexMinus,
    ) = fl.FibonacciSpectrum(
        TotalTimeTranslations,
        TimeSteps,
        Size,
        SeedMinus,
        NumberOfSubstitutions,
        BoundaryLenght,
        DecisionFactor,
        MassFactor,
    )

    NumberOfLabels = 15
    fig, ax = plt.subplots(figsize=(25, 25))
    MaxEigenval = np.nanmax(FullSpectrumPlus)
    MinEigenVal = np.nanmin(FullSpectrumPlus)
    EigenValuesAxis = np.linspace(MinEigenVal, MaxEigenval, NumberOfLabels)
    TimeAxis = np.outer(range(TotalNumberOfSteps), np.ones(Size) / TimeSteps)
    FormatTimes = [
        f"{value:.2f}"
        for value in np.linspace(0, TotalTimeTranslations, NumberOfLabels)
    ]
    FormatEigenValues = [
        f"{value:.2f}"
        for value in np.linspace(MinEigenVal, MaxEigenval, NumberOfLabels)
    ]
    ax.scatter(
        TimeAxis,
        FullSpectrumPlus,
        marker=".",
        s=1,
        linewidths=0.5,
        color="black",
        rasterized=True,
    )
    ax.scatter(
        LeftIndexPlus,
        LeftSpectrumPlus,
        marker=".",
        s=1,
        linewidths=0.5,
        color="lime",
        rasterized=True,
    )
    ax.scatter(
        LeftIndexMinus,
        LeftSpectrumMinus,
        marker=".",
        s=1,
        linewidths=0.5,
        color="red",
        alpha=0.5,
        rasterized=True,
    )

    ax.set_xticks(np.linspace(0, TotalTimeTranslations, NumberOfLabels))
    ax.set_xticklabels(FormatTimes)
    ax.set_yticks(np.linspace(MinEigenVal, MaxEigenval, NumberOfLabels))
    ax.set_yticklabels(FormatEigenValues)
    ax.set_xlabel("#translations")
    ax.set_ylabel("Energy")

    stop = timeit.default_timer()
    print("Execution time:  ", stop - start)

    plt.show()


if __name__ == "__main__":
    main()
