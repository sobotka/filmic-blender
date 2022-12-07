#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy


def as_numeric(a, dtype=None):
    if dtype is None:
        dtype = float

    try:
        return dtype(a)
    except (TypeError, ValueError):
        return a


def adjust_exposure(RGB_input, exposure_adjustment):
    return numpy.power(2.0, exposure_adjustment) * RGB_input


def apply_display_inverse_EOTF(RGB_input, display_EOTF):
    return numpy.power(RGB_input, (1.0 / display_EOTF))


def open_domain_to_normalized_log2(
    in_od, in_middle_grey=0.18, minimum_ev=-7.0, maximum_ev=+7.0
):
    total_exposure = maximum_ev - minimum_ev

    in_od = numpy.asarray(in_od)
    in_od[in_od <= 0.0] = numpy.finfo(float).eps

    output_log = numpy.clip(
        numpy.log2(in_od / in_middle_grey), minimum_ev, maximum_ev
    )

    return as_numeric((output_log - minimum_ev) / total_exposure)


def normalized_log2_to_open_domain(
    in_norm_log2, od_middle_grey=0.18, minimum_ev=-7.0, maximum_ev=+7.0
):
    in_norm_log2 = numpy.asarray(in_norm_log2)

    in_norm_log2 = (
        numpy.clip(in_norm_log2, 0.0, 1.0) * (maximum_ev - minimum_ev)
        + minimum_ev
    )

    return as_numeric(numpy.power(2.0, in_norm_log2) * od_middle_grey)


def linear_breakpoint(numerator, slope, coordinate):
    denominator = numpy.ma.power(
        numpy.ma.power(slope, 2.0).filled(fill_value=0.0) + 1.0, 1.0 / 2.0
    ).filled(fill_value=0.0)

    return numpy.ma.divide(numerator, denominator) + coordinate


def line(x_in, slope, intercept):
    return numpy.ma.add(numpy.ma.multiply(slope, x_in), intercept)


def scale(limit_x, limit_y, transition_x, transition_y, power, slope):
    term_a = numpy.ma.power(
        numpy.ma.multiply(slope, numpy.ma.subtract(limit_x, transition_x)),
        -power,
    ).filled(fill_value=0.0)

    term_b = numpy.ma.subtract(
        numpy.ma.power(
            numpy.ma.divide(
                numpy.ma.multiply(
                    slope, numpy.ma.subtract(limit_x, transition_x)
                ),
                numpy.ma.subtract(limit_y, transition_y),
            ),
            power,
        ).filled(fill_value=0.0),
        1.0,
    )

    return numpy.ma.power(
        numpy.ma.multiply(term_a, term_b), -numpy.ma.divide(1.0, power)
    ).filled(fill_value=0.0)


def exponential(x_in, power):
    return numpy.ma.divide(
        x_in,
        numpy.ma.power(
            numpy.ma.add(1.0, numpy.ma.power(x_in, power)),
            numpy.ma.divide(1.0, power),
        ),
    )


def exponential_curve(x_in, scale, slope, power, transition_x, transition_y):
    return numpy.ma.add(
        numpy.ma.multiply(
            scale,
            exponential(
                numpy.ma.divide(
                    numpy.ma.multiply(
                        slope, numpy.ma.subtract(x_in, transition_x)
                    ),
                    scale,
                ),
                power,
            ),
        ),
        transition_y,
    )


def calculate_sigmoid(
    # Input x
    x_in,
    # Pivot coordinates x and y for the fulcrum.
    pivots,
    # Slope of linear portion.
    slope,
    # Length of transition toward the toe and shoulder.
    lengths,
    # Exponential power of the toe and shoulder regions.
    powers,
    # Intersection limit coordinates x and y for the toe and shoulder.
    limits,
    debug=False,
):
    # t_tx
    transition_toe_x = linear_breakpoint(-lengths[0], slope, pivots[0])
    if debug is True:
        print("transition_toe_x: {}".format(transition_toe_x))

    # t_ty
    transition_toe_y = linear_breakpoint(
        numpy.ma.multiply(slope, -lengths[0]), slope, pivots[1]
    )
    if debug is True:
        print("transition_toe_y: {}".format(transition_toe_y))

    # s_tx
    transition_shoulder_x = linear_breakpoint(lengths[1], slope, pivots[0])
    if debug is True:
        print("transition_shoulder_x: {}".format(transition_shoulder_x))

    # s_ty
    transition_shoulder_y = linear_breakpoint(
        numpy.ma.multiply(slope, lengths[1]), slope, pivots[1]
    )
    if debug is True:
        print("transition_shoulder_y: {}".format(transition_shoulder_y))

    # t_itx
    inverse_transition_toe_x = numpy.ma.subtract(1.0, transition_toe_x)
    if debug is True:
        print("inverse_transition_toe_x: {}".format(inverse_transition_toe_x))

    # t_ity
    inverse_transition_toe_y = numpy.ma.subtract(1.0, transition_toe_y)
    if debug is True:
        print("inverse_transition_toe_y: {}".format(inverse_transition_toe_y))

    # t_ilx
    inverse_limit_toe_x = numpy.ma.subtract(1.0, limits[0, 0])
    if debug is True:
        print("inverse_limit_toe_x: {}".format(inverse_limit_toe_x))

    # t_ily
    inverse_limit_toe_y = numpy.ma.subtract(1.0, limits[0, 1])
    if debug is True:
        print("inverse_limit_toe_y: {}".format(inverse_limit_toe_y))

    scale_toe = -scale(
        limit_x=inverse_limit_toe_x,
        limit_y=inverse_limit_toe_y,
        transition_x=inverse_transition_toe_x,
        transition_y=inverse_transition_toe_y,
        power=powers[0],
        slope=slope,
    )
    if debug is True:
        print("scale_toe: {}".format(scale_toe))

    scale_shoulder = scale(
        limit_x=limits[1, 0],
        limit_y=limits[1, 1],
        transition_x=transition_shoulder_x,
        transition_y=transition_shoulder_y,
        power=powers[1],
        slope=slope,
    )
    if debug is True:
        print("scale_shoulder: {}".format(scale_shoulder))

    # b
    intercept = numpy.ma.subtract(
        transition_toe_y, numpy.ma.multiply(slope, transition_toe_x)
    )

    return numpy.where(
        x_in < transition_toe_x,
        exponential_curve(
            x_in,
            scale_toe,
            slope,
            powers[0],
            transition_toe_x,
            transition_toe_y,
        ),
        numpy.where(
            x_in <= transition_shoulder_x,
            line(x_in, slope, intercept),
            exponential_curve(
                x_in,
                scale_shoulder,
                slope,
                powers[1],
                transition_shoulder_x,
                transition_shoulder_y,
            ),
        ),
    )
