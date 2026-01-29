import FibonacciLattice as fl
import numpy as np
import matplotlib.pyplot as plt
import timeit


def main():
    start = timeit.default_timer()
    N = 10
    Seed = "0,0"
    Size = 70
    Mass = 1
    Translations = 50
    TimeSteps = 100

    FullSpectrum = fl.FullSpectrum(Size, Mass, Seed, N, TimeSteps, Translations)
    Map = np.outer(range(Translations * TimeSteps), np.ones(Size) / TimeSteps)
    fig, ax = plt.subplots(figsize=(25, 25))

    ax.scatter(
        Map,
        FullSpectrum,
        marker=".",
        s=1,
        linewidths=0.5,
        color="black",
        rasterized=True,
    )

    plt.show()

    stop = timeit.default_timer()
    print("Time: ", stop - start)


if __name__ == "__main__":
    main()
