# 4. Map Your Place by Driving the Robot

Video: [Map your room Step by Step using Arduino/ROS2 self-driving robot](https://youtu.be/7uo4BGxWHCA)
{: .video-link }

In this chapter you drive the robot around your home from the PC keyboard while ROS2 builds a map
from its LiDAR scans, then save the map to your PC. In the next chapter the robot uses this map to
drive itself.

You need the robot assembled, flashed and connected (chapters 1–3), plus Docker Desktop, VcXsrv
and PowerShell on your Windows PC. Mapping one or two rooms takes about 15–30 minutes.

![The robot maps rooms with its LiDAR, then drives itself using that map.](yt:7uo4BGxWHCA@0:05)

## Prepare your place

A LiDAR sees one thin horizontal slice at the height of its laser, so some things are invisible
to it.

!!! update "Since the video was recorded"
    - Block off objects the LiDAR cannot detect, for example with cardboard: black
      (non-reflective), transparent, too low to reach the laser plane, very thin or sparse (fine
      mesh), lit brightly by near-infrared light (sunlight, incandescent bulbs), and mirrors or
      highly reflective objects.
    - The robot can't drive over thick carpet or thresholds higher than about 5 mm (1/5″).
    - Keep the scene static while mapping; for example, don't open or close doors.
    - Declutter and leave plenty of space between obstacles.
    - Block off angled ramps. A ramp tilts the laser plane and spoils the map.

## Launch the robotics software

1. Make sure Docker Desktop is running.

2. Start the X server, which RViz needs to open its window: run XLaunch, keep **Multiple
   windows**, set **Display number** to `0`, click **Next** through the rest and **Finish**. Its
   icon appears in the system tray.

    ![In XLaunch, set the Display number to zero.](yt:7uo4BGxWHCA@0:50#crop=0.05,0,0.9,0.62)

3. Launch Windows PowerShell.
4. Click in the PowerShell window and press **Alt+Shift+-** to split it horizontally. Repeat until
   you have three panes: top, middle and bottom.

5. In the **top** window, launch the robotics software:

    ```
    docker run --name makerspet -it --rm -v c:\maps:/root/maps -p 8888:8888/udp -p 4430:4430/tcp -e DISPLAY=host.docker.internal:0.0 -e LIBGL_ALWAYS_INDIRECT=0 kaiaai/kaiaai:iron
    ```

    Compared with Chapter 3, this adds `-v c:\maps:/root/maps`, which shares `C:\maps` on Windows
    with `/root/maps` (`~/maps`) in the container. Without it, `--rm` would delete your map when
    the container exits.

    ![Start the Docker image with the maps folder shared.](yt:7uo4BGxWHCA@1:23)

6. In the **middle** and **bottom** windows, open shells in the same container:

    ```
    docker exec -it makerspet bash
    ```

    Each shows a `root@...:/ros_ws#` prompt.

    ![Open two more shells with docker exec.](yt:7uo4BGxWHCA@1:30)

7. Click `https://github.com/kaiaai/kaiaai` in the startup message and scroll to
   **Command cheat sheets** › **Operate a physical robot** to copy and paste commands.

    ![The cheat sheet for a physical robot.](yt:7uo4BGxWHCA@1:44#crop=0,0,0.42,1)

## Bring up the robot

1. In the **top** window, start ROS2 and the micro-ROS agent the robot connects to:

    ```
    ros2 launch kaiaai_bringup physical.launch.py
    ```

    ![Launch ROS2 and micro-ROS in the top window.](yt:7uo4BGxWHCA@1:52)

2. Turn the robot on and place it on the floor.

    <div class="pair" markdown="1">
    ![Turn the power switch on.](yt:7uo4BGxWHCA@1:58)
    ![Place the robot on the floor.](yt:7uo4BGxWHCA@2:02)
    </div>

3. Once the robot connects, the top window prints its messages, including the LiDAR model.

    ![The robot has connected.](yt:7uo4BGxWHCA@2:07#crop=0.59,0,0.41,0.28)

!!! note
    Occasional `message(s) lost` and `RESULT_CRC_ERROR` lines are normal over WiFi. To keep them
    rare, give the robot a strong WiFi signal and keep the network quiet while the robot runs: for
    example, don't stream video on another PC or phone on the same WiFi.

## Start teleoperation and mapping

1. In the **bottom** window, launch keyboard teleoperation:

    ```
    ros2 run kaiaai_teleop teleop_keyboard
    ```

    ![Launch teleoperation in the bottom window.](yt:7uo4BGxWHCA@2:15)

2. In the **middle** window, launch Nav2 with SLAM (simultaneous localization and mapping) and
   RViz:

    ```
    ros2 launch kaiaai_bringup navigation.launch.py slam:=True
    ```

    ![Launch mapping in the middle window.](yt:7uo4BGxWHCA@2:27)

3. RViz opens after a few seconds and shows the map starting to form.

    ![The map starts to form around the robot.](yt:7uo4BGxWHCA@2:38)

!!! note
    The command reference also lists `ros2 launch kaiaai_bringup cartographer.launch.py` under
    "Create a map while driving manually". The video uses `navigation.launch.py slam:=True`.

## Drive around and map your place

1. Click in the **bottom** window so it receives your key presses.
2. Drive the robot:

    | Key | Action |
    |---|---|
    | `w` / `x` | increase / decrease linear (forward) velocity |
    | `a` / `d` | increase / decrease angular (turning) velocity |
    | `s` | keep straight |
    | `CAPS` | large step |
    | `Space` | force stop |
    | `CTRL-C` | quit |

    Keys change speed in steps; the robot keeps moving until you change it or press `Space`.

    ![The teleoperation keys.](yt:7uo4BGxWHCA@2:30#crop=0.59,0.52,0.41,0.38)

3. Drive as slowly as possible. The video uses 0.05 m/s and 0.2 rad/s, one or two key presses
   from a standstill.

    ![Drive slowly for a better map.](yt:7uo4BGxWHCA@2:53)

4. Visit every room, following walls and circling furniture, until the map has no gaps.

    ![The map grows as the robot explores (16× speed).](yt:7uo4BGxWHCA@3:10)

!!! update "Since the video was recorded"
    **Map skewed or distorted?** Drive and turn slowly; fast motion skews SLAM badly. Check the
    sensors with `ros2 launch kaiaai_bringup monitor_robot.launch.py`, and start with a simple room
    (one central obstacle).

    **Map distorts or the robot drifts off it?** The wheel speed probably doesn't match the
    command, usually due to a wrong encoder PPR (pulses per revolution) in `config.yaml`. Read it
    with `ros2 param get /pet motor.encoder.ppr`. To measure it, count encoder ticks over one wheel
    revolution and divide by 4 (the firmware multiplies PPR by 4 for quadrature edges). Set the
    correct PPR and a reachable Max RPM, then re-upload the sketch data.

    **Scan slides sideways when driving straight?** If rotation looks right and odometry is
    calibrated, the LiDAR is mounted rotated relative to its URDF frame. Add the yaw offset to the
    laser joint's rpy; for a LiDAR mounted 180° around, add 3.14 rad.

## Save your map and shut down

1. Click in the **bottom** window and press **Ctrl+C** to stop teleoperation.

2. In the same window, save the map:

    ```
    ros2 run nav2_map_server map_saver_cli -f ~/maps/map --ros-args -p save_map_timeout:=60.0
    ```

    This writes `map.pgm` (the image) and `map.yaml` (resolution and origin) to `C:\maps`. Wait
    for `Map saved successfully`.

    ![Save the map.](yt:7uo4BGxWHCA@4:23.5)

    ![Map saved successfully.](yt:7uo4BGxWHCA@4:25#crop=0.59,0.52,0.41,0.48)

3. Press **Ctrl+C** in the middle and top windows and wait for the processes to finish.

    ![Terminate all tasks with Ctrl+C.](yt:7uo4BGxWHCA@4:30)

4. Type `exit` in each shell and close PowerShell.
5. Turn off the robot.

!!! update "Since the video was recorded"
    `--rm` discards changes made inside the container (your map is safe in `C:\maps`). To keep
    other changes, such as edited config files, commit the running container from another
    PowerShell window *before* exiting it:

    ```
    docker container commit makerspet kaiaai/kaiaai:iron
    ```

    Don't commit or publish an image that contains secrets such as your WiFi credentials.

## View your map

1. Open File Explorer and type `C:\maps` into the address bar.

    ![Go to C:\maps in File Explorer.](yt:7uo4BGxWHCA@4:58#crop=0,0.33,1,0.67)

    ![map.pgm and map.yaml.](yt:7uo4BGxWHCA@5:03#crop=0,0.33,1,0.45)

2. Open `map.pgm` in a PGM-capable viewer: GIMP for Windows (https://www.gimp.org/downloads/), as
   in the video, or the lighter XnView. White is free space, black is obstacles, gray is
   unexplored.

    ![The map in GIMP.](yt:7uo4BGxWHCA@5:12)

3. If the map appears rotated, use **View › Flip & Rotate › Rotate 90° counter-clockwise** (or
   whichever fits) in GIMP.
   This rotates the view, not the file.

    ![Rotate the view in GIMP.](yt:7uo4BGxWHCA@5:18)

!!! tip
    Don't edit and re-save `map.pgm`. The robot uses it, with `map.yaml`, in the next chapter.

A clean map has straight walls, closed outlines and few stray specks. If yours is much messier,
declutter, drive slower and map again.

![A clean map.](https://makerspet.com/wp-content/uploads/2026/04/clean_map.webp)

Next: let the robot drive itself using this map.
