What?
=====

This OpenColorIO configuration adds a closer-to-photorealistic view transform for your renders. For imagers working with non-photorealistic rendering, it also will bring significant dynamic range and lighting capabilities to your work.

Why?
====

Because the basic sRGB EOTF was never designed for rendering and should be avoided. This configuration
is as close as one will get to a magic button to help an imager elevate their rendering immediately.

How?
====

 1. Download this repository. Replace your current OpenColorIO configuration in Blender with this version.
The Blender OpenColorIO configuration directory is located in:

        BLENDER/bin/VERSIONNUMBER/datafiles/colormanagement

    Move the existing ````colormanagement```` directory to a backup location, and place the contents of
    this repository into a new ````colormanagement```` directory.
    
    Optionally, instead of replacing the actual directory, use the envrionment variable to specify where the OCIO configuration lives:

        export OCIO=/path/to/where/the/filmic-blender/config.ocio
 1. From within the Color Management panel, change the View to your desired contrast level and render.
