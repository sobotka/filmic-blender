#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sigmoid_module
import numpy
import pandas
import scipy
import matplotlib
from matplotlib import pyplot

if __name__ == "__main__":

    contrasts = [
        "Very Low Contrast",
        "Medium Low Contrast",
        "Low Contrast",
        "Base Contrast",
        "Medium High Contrast",
        "High Contrast",
        "Very High Contrast",
    ]

    filmic_contrasts = pandas.read_csv(
        "./data/filmic-contrasts.csv", names=contrasts
    )

    def solver_function(
        x_in, slope, distance_toe, distance_shoulder, power_toe, power_shoulder
    ):
        return sigmoid_module.calculate_sigmoid(
            x_in,
            pivots=[10.0 / 16.5, 0.5],
            slope=slope,
            lengths=[distance_toe, distance_shoulder],
            powers=[power_toe, power_shoulder],
            limits=numpy.asarray([[0.0, 0.0], [1.0, 1.0]]),
        )

    x_input = numpy.linspace(0.0, 1.0, len(filmic_contrasts))

    fit_parameters = []
    fit_errors = []

    for contrast_curve in filmic_contrasts:
        popt, pcov = scipy.optimize.curve_fit(
            f=solver_function,
            xdata=x_input,
            ydata=filmic_contrasts[contrast_curve],
            p0=[2.2, 0.2, 0.2, 2.0, 2.0],
            bounds=(0.0, [5.0, 1.0, 1.0, 5.0, 5.0]),
        )
        fit_parameters.append(popt)

        error = numpy.sqrt(numpy.diag(pcov))
        fit_errors.append(error)

        print(
            "Filmic {}:\n\tslope({})\n\tdistance toe({})\n\t"
            "distance shoulder({})\n\tpower toe({})\n\t"
            "power shoulder({})\n\terror:({})".format(
                contrast_curve,
                popt[0],
                popt[1],
                popt[2],
                popt[3],
                popt[4],
                error,
            )
        )

    figure = pyplot.figure(figsize=(10, 10), dpi=72)
    figure.patch.set_alpha(1.0)
    axes = figure.add_subplot()
    axes.set_aspect("equal", adjustable="box")
    axes.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=0.1))
    axes.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(base=0.05))
    axes.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=0.1))
    axes.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(base=0.05))
    pyplot.grid(visible=True, which="minor", axis="both", color="gainsboro")
    pyplot.grid(visible=True, which="major", axis="both", color="slategrey")
    axes.tick_params(
        axis="both", which="both", colors="slategrey", labelsize=8
    )

    for index, fit_parameter in enumerate(fit_parameters):
        (
            slope,
            distance_toe,
            distance_shoulder,
            power_toe,
            power_shoulder,
        ) = fit_parameter
        result_curve = solver_function(
            x_input,
            slope,
            distance_toe,
            distance_shoulder,
            power_toe,
            power_shoulder,
        )

        legend = "{}\nError: {}".format(contrasts[index], fit_errors[index])
        axes.plot(x_input, result_curve, label=legend)

    for contrast in filmic_contrasts:
        axes.plot(x_input, filmic_contrasts[contrast])

    pyplot.xlabel("Input Filmic Log Encoding Base")
    pyplot.ylabel("Output Display 2.2 EOTF Encoded")
    pyplot.title("Filmic Contrasts Curve Fitting Demonstration")
    pyplot.legend()
    pyplot.show()
