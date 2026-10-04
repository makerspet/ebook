# Appendix D. 3D Print the Robot Parts

The robot's plastic parts are open source. If you have a 3D printer, you can print them instead of
buying them. The electronics, motors and hardware still come from the build pack or your own
sources.

## Get the files

Download the files from the "Download Files for 3D Printing" section of the build guide at
[makerspet.com/blog/bld-120mm-pack](https://makerspet.com/blog/bld-120mm-pack/). That page always
has the latest versions:

- **3MF files** for the base, LiDAR skirts, LiDAR posts, board posts, caster roller, caster mounts
  and the 2S battery holder backstop
- **3MF files** for the wheels
- **3MF files** for the motor clamps
- The full **Autodesk Fusion 360** model (`.f3d`), if you want to modify the design

The base takes the Maker's Pet ESP32-E dev kit module.

## Slicer settings

Set **Seam Position** to **Random** in your slicer for the **caster roller** and the **wheels**.
With an aligned seam, the caster roller knocks rhythmically as it rolls and the wheels make the
robot wobble slightly.

## Parts you don't print

From the build pack list in Chapter 1, these aren't printed:

- BDC-30P driver board and Maker's Pet ESP32-E 30-pin dev kit module
- LDROBOT LD14P LiDAR and its breakout cable
- Two N20 gear motors with encoders, and two motor cables
- Two tires and the roller's metal shaft
- Battery case for 6 AA batteries
- M3 screws: countersunk and hex button

## Optional: 18650 battery holder mod

The 2×18650 mod uses two printed parts from the same file set: the **battery holder backstop** and
the **wider LiDAR skirt**. Chapter 1 shows how to assemble it, with the safety warnings for
rechargeable cells.
