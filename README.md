# [Download the latest version of Filmic Blender](https://github.com/sobotka/filmic-blender/archive/master.zip)

# Who?

This is a simple OpenColorIO configuration for intermediate to advanced imagers using Blender's Cycles raytracing engine.

# What?

This OpenColorIO configuration adds a closer-to-photorealistic view transform for your renders. For imagers working with non-photorealistic rendering, it also will bring significant dynamic range and lighting capabilities to your work, as well as potentially open up correct transforms for rendering to HDR displays and other such forward looking technology. It is as close to a Magic Button™ you can get for an experienced imager. The kit embodies a high dynamic range transfer function and an intensity gamut mapping.

# When?

This repository is ready to use right now, with no compilation or special Blender application binaries required.

# Why?

Because the basic sRGB nonlinear transfer functions (OETF / EOTF) were designed to describe an aspect of device response and never for rendering. This configuration is a step towards providing imagers with a reliable camera rendering transform and a base of aesthetic looks useful for modern raytracing engine CGI, animation, and visual effects work with real-world cameras.

# How?

1. [Download the latest version of Filmic Blender](https://github.com/sobotka/filmic-blender/archive/master.zip). Replace your current OpenColorIO configuration in Blender with this version.
 1. The Blender OpenColorIO configuration directory is located in:

        BLENDER/bin/VERSIONNUMBER/datafiles/colormanagement

    Move the existing ````colormanagement```` directory to a backup location, and place the contents of
    this repository into a new ````colormanagement```` directory.

 1. Optionally, instead of replacing the actual directory, use the environment variable to specify where the OCIO configuration lives:

        export OCIO=/path/to/where/the/filmic-blender/config.ocio

1. From within the Color Management panel, change the View to your desired contrast level and render.

Once you have Blender utilising the configuration, you are free to render away. You may discover that some of your materials were broken due to exceptionally low lighting levels, and may require reworking. General PBR advice holds true when using wider and more photographic illumination levels.

# Supported Display Colorimetry

The current configuration supports:
 * Generic sRGB / REC.709 displays with 2.2 native power function
 * Display P3 displays with 2.2 native power function. Examples include:
   * Apple MacBook Pros from 2016 on.
   * Apple iMac Pros.
   * Apple iMac from late 2015 on.
 
Due to an unfortunate side effect of the way Blender has thus far integrated colour management, folks pushing pixels on Apple Display P3 devices will need to be careful when encoding images. Loosely:
 * When viewing renders, use the Apple Display P3 setting.
 * When saving nonlinear display referred files such as JPEG, TIFF, etc. it is critical that the Display be set to the file encoding. For example, for sRGB imagery, the View must be set to sRGB for the file to be properly encoded. **If this is not done, the file will not be encoded properly**. [The bug / todo can be found at the link provided](https://developer.blender.org/T58805).

# Additional Information and Technical Details

The basic kit of weaponry includes:

## View Transforms

A set of View transforms that include:

 1. ***sRGB OETF***. This is an accurate version of the sRGB transfer function. This is identical to what imagers would use as the "Default" View transform in Blender proper. Should be avoided at all costs for CGI work. Useful in some edge cases for albedo textures, for example.
 1. ***Non-Colour Data***. This is a view useful for evaluating a data format. Do not expect to see perceptual values however, as it is literally data dumped directly to the screen. Use this transform on your buffer, via the *UV Image Viewer* Properties panel, if your buffer represents data and not colour information. This will keep it out of the OpenColorIO transformation pipeline chain and leave it as data.
 1. ***Linear Raw***. This is a colour managed linearized version of your data. For all intents an purposes, will look identical to ***Non-Colour Data***, but applied to colour based data such as an image.
 1. ***Filmic Log Encoding Base***. This is the workhorse View for all of your rendering work. Setting it in the View will result in a log encoded appearance, which will look exceptionally low contrast. Use this if you want to adjust the image for grading using another tool such as Resolve, with no additional modifications. Save to a high bit depth display referred format such as 16 bit TIFF. This basic view is designed to be coupled with one of the contrast looks.

## Look Transforms

A set of Look transforms that include:

 1. ***Greyscale***. This Look is based off of the ***Filmic Log Encoding Base*** and will deliver a weighted greyscale version of the image. The weights used are for REC.709 RGB lights, which are the same lights specified in sRGB.
 1. Five contrast base looks for use with the ***Filmic Log Encoding Base***. All map middle grey 0.18 to 0.5 display referred. Each has a smooth roll off on the shoulder and toe. They include:
    1. ***Very High Contrast***.
    1. ***High Contrast***.
    1. ***Medium High Contrast***.
    1. ***Base Contrast***. Similar to the sRGB contrast range, with a smoother toe.
    1. ***Medium Low Contrast***.
    1. ***Low Contrast***.
    1. ***Very Low Contrast***.
 1. ***False Colour***. This Look is an extremely useful tool for evaluating your image in terms of the dynamic range and latitude. It is a colour coded "heat map" of your image values, according to the following codes:

    | Value | Colour | Scene Referred Value |
    | ---- | ---- | ---- |
    | Low Clip | Black | Scene Referred Linear value below 0.0001762728758. |
    | -10 EV | Purple | Scene Referred Linear value 0.0001762728758. |
    | -7 EV | Blue | Scene Referred Linear value 0.001404109349. |
    | -4 EV | Cyan | Scene Linear value 0.01124714399. |
    | -2 EV | Green | Scene Referred Linear value 0.04456791864. |
    | 0 EV| Grey | Scene Referred Linear value 0.18009142. |
    | +2 EV | Green | Scene Referred Linear value 0.7196344767. |
    | +4 EV | Yellow | Scene Referred Linear value 2.883658483. |
    | +5.5 EV | Red | Scene Referred Linear value 8.150007644. |
    | High Clip | White | Scene Referred Linear value above 16.29174024. |

# Grading Your Work

Given that images generated under Cycles are scene referred, many nodes in Blender, being broken, will not work properly. This may have been hidden if one used a range that perfectly mapped to the display referred domain such as the sRGB transfer function, however using a proper camera rendering transform exacerbates this brokenness.

There are a good number of nodes that work absolutely fine. For grading, it is highly encouraged to use the ASC CDL node, as it operates on scene referred imagery perfectly well. It is in the ***Color -> Color Balance*** node. Do **not** use the ***Lift, Gamma, Gain*** default as it is strictly a display referred formula and will break on scene referred imagery. Instead, change the drop down to ***ASC CDL*** and use the *Slope*, *Offset*, and *Power* controls to perform grading.

Almost all of the Adobe PDF specification blend modes in the ***Mix*** node are also display referred and are broken for Cycles rendering. That includes but is not limited to Overlay, Screen, and other such modes.

# Viewing in Other Applications

It is important to tag your imagery generated with Filmic with the canonized sRGB ICC for viewing outside of Blender and across applications and the web. Simply assign the profile to your generated image using the tool of your choice. Do not convert.

# Colorimetric Information

## RGB Primaries

Filmic was designed to be easily integrated into existing pipelines, and as such, uses the primaries and achromatic white colour outlined in ITU-R BT.709 specification. As a result, the reference space lights match the sRGB specification and are as follows:

| Primary | x | y |
| -- | -- | -- |
| Red | 0.64 | 0.33 |
| Green | 0.30 | 0.60 |
| Blue | 0.15 | 0.06 |
| Achromatic | 0.3127 | 0.3290 |

## RGB to XYZ transform

Following with the above, the transformation for primaries to the CIE 1931 2 degree standard observer XYZ model, is:

| Primary | Red | Green | Blue |
| -- | -- | -- | -- |
| X | 0.4123910 | 0.3575840 | 0.1804810 |
| Y | 0.2126390 | 0.7151690 | 0.0721923 |
| Z | 0.0193308 | 0.1191950 | 0.9505320 |

## Transfer Function of Base Log Encoding

The canonized ground-truth encoding for Filmic is the *Filmic Base Log Encoding*. The Base Log Encoding is a pure normalized log 2 encoding in two parts, to accomodate the gamut mapping for wide primary ratio intensity gamut mapping. The first portion that is routed through the 3D LUT for the gamut compression at value range `-12.473931188, 12.526068812`. The final *Base Log Encoding* covers the log 2 range of `-12.473931188, 4.026068812`.

## Transfer Function of Aesthetic Outputs

The contrasts are designed for an idealized sRGB display, with the aforementionned primaries, and an Electro-Optical Transfer Function consisting of a pure 2.2 power function.

# Issues

Please post any and all issues to the issue tracker at GitHub.
