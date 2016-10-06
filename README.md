What?
=====

This OpenColorIO configuration adds a closer-to-photorealistic view transform for your renders.

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
 1. From within the Color Management panel, change the View to your desired contrast level and render.
