# 5. Let the Robot Explore and Self-Drive

Video: [Arduino/ROS2 robot self-drives - operation instructions](https://youtu.be/81-9q7QfkHs)
{: .video-link }

Now your robot drives itself. First it explores your place and builds a map. Then you save the map
and click any spot in RViz; the robot plans a path, drives there and steers around obstacles.

Your robot should be assembled, brought up and connected to WiFi and your PC. Chapter 4 helps: it
uses the same Docker image, terminals and RViz. Allow about 30 minutes, mostly watching the robot
explore.

![The robot self-drives under a chair; RViz shows the map and planned path.](yt:RCPUQmvS37Q@0:14)

## Prepare your place

The LiDAR sees obstacles only in one horizontal plane, at sensor height; anything lower is
invisible. The robot also gets stuck on thick carpet and high thresholds.

1. Remove low objects, or block them with cardboard so the LiDAR can see them.
2. Remove or block off thick carpet and high thresholds.

![Block low obstacles with cardboard, or remove them.](yt:81-9q7QfkHs@0:44)

![Remove thick carpet.](yt:81-9q7QfkHs@0:46)

!!! update "Since the video was recorded"
    Also prepare the following:

    - Block (for example, with cardboard) objects the LiDAR cannot detect: black (non-reflective),
      transparent, too low for the laser plane, too small (such as fine sparse mesh), mirrors and
      highly reflective objects, and objects under bright near-infrared light (sunlight,
      incandescent bulbs).
    - The robot cannot drive over thick carpet or thresholds higher than about 5 mm (1/5″).
    - Keep the scene static while mapping; for example, don't open or close doors.
    - Declutter and leave plenty of space between obstacles.
    - Block off angled ramps: they tilt the LiDAR's laser plane and mess up the map.

## Launch the robotics software

You will use three command windows: one for the Docker container and the robot link, one for
mapping and navigation, and one for exploration and saving the map.

1. Open Windows PowerShell, click in its window and press **Alt+Shift+-** to split it horizontally.
   Repeat until you have three panes: top, middle and bottom.

2. In the top window, launch the Docker image:

    ```
    docker run --name makerspet -it --rm -v c:\maps:/root/maps -p 8888:8888/udp -p 4430:4430/tcp -e DISPLAY=host.docker.internal:0.0 -e LIBGL_ALWAYS_INDIRECT=0 kaiaai/kaiaai:iron
    ```

   `-v c:\maps:/root/maps` shares `c:\maps` on your PC with the container, so your saved map
   survives when the container stops.

![Launch the Docker image in the top window.](yt:81-9q7QfkHs@1:16)

!!! tip
    Start the X server first: launch **XLaunch** from your desktop with display number `0`
    (Chapter 2). Without it, RViz can't open its window.

!!! update "Since the video was recorded"
    A ROS 2 Jazzy image, `kaiaai/kaiaai:jazzy`, is also available next to `kaiaai/kaiaai:iron`.
    To use it, change the tag at the end of the command.

3. Ctrl-click the help link `https://github.com/kaiaai/kaiaai` that the container prints. Every
   command in this chapter is under **Command cheat sheets** there, ready to copy and paste.

![Ctrl-click the help link to open the command reference.](yt:81-9q7QfkHs@1:24)

4. In each of the other two windows, open a Bash shell inside the container:

    ```
    docker exec -it makerspet bash
    ```

![Open a Bash shell in the middle and bottom windows.](yt:81-9q7QfkHs@1:30)

## Connect to your robot

1. In the top window, launch communication with your robot:

    ```
    ros2 launch kaiaai_bringup physical.launch.py
    ```

![Launch robot communication in the top window.](yt:81-9q7QfkHs@1:48)

2. Turn your robot on and place it on the floor. Once it connects to WiFi and your PC, the top
   window prints its messages.

![The robot is connected: the top window shows its messages.](yt:81-9q7QfkHs@2:02)

## Let the robot explore and create a map

1. In the middle window, launch mapping, navigation and visualization. `slam:=True` builds a new
   map while navigating (SLAM: simultaneous localization and mapping):

    ```
    ros2 launch kaiaai_bringup navigation.launch.py slam:=True
    ```

![Launch mapping and navigation in the middle window.](yt:81-9q7QfkHs@2:14)

2. RViz opens with the start of the map and the **Navigation 2** panel on the left.

![RViz with the start of the map and the Navigation 2 panel.](yt:81-9q7QfkHs@2:24#crop=0.18,0,0.82,1)

3. In the bottom window, launch exploration:

    ```
    ros2 launch explore_lite explore.launch.py
    ```

![Launch exploration in the bottom window.](yt:81-9q7QfkHs@2:34)

4. Watch your robot explore. The software keeps sending it to *frontiers*, the edges between mapped
   and unknown areas, until nothing is left to explore.

![The map grows as the robot explores.](yt:81-9q7QfkHs@2:52)

5. When no frontiers are left, the robot returns to its start and the bottom window reports
   `All frontiers traversed/tried out, stopping.`

![Exploration finished: the map is complete.](yt:81-9q7QfkHs@2:56)

## Save the map

1. Press Ctrl-C in the bottom window to stop exploration.

2. In the same window, save the map:

    ```
    ros2 run nav2_map_server map_saver_cli -f ~/maps/map --ros-args -p save_map_timeout:=60.0
    ```

3. Look for `Map saved successfully`. The map is two files, `/root/maps/map.pgm` (the image) and
   `/root/maps/map.yaml` (its settings), also in `c:\maps` on your PC.

![The map saver reports success.](yt:81-9q7QfkHs@3:24#crop=0.615,0.52,0.385,0.48)

## Send the robot to a destination

Navigation is still running with your new map, so you can send the robot places right away.

1. Click **Nav2 Goal** in the RViz toolbar.

![Click Nav2 Goal.](yt:81-9q7QfkHs@3:24)

2. Click and hold on the map where you want the robot to go.
3. Drag to set the direction it should face on arrival (the green arrow).
4. Release and watch your robot self-drive.

<div class="pair" markdown="1">
![Click and hold on the destination.](yt:81-9q7QfkHs@3:26)
![Drag to set the orientation, then release.](yt:81-9q7QfkHs@3:28)
</div>

![The robot follows the planned path (the thin line) to the goal.](yt:81-9q7QfkHs@3:30)

5. Try a few more destinations.

## Self-drive using the saved map

Next time, skip exploring and load the saved map.

1. Press Ctrl-C in the middle window to stop mapping and navigation.

2. In the middle window, launch navigation with your saved map:

    ```
    ros2 launch kaiaai_bringup navigation.launch.py map:=$HOME/maps/map.yaml
    ```

![Launch navigation with the saved map.](yt:81-9q7QfkHs@4:06)

3. RViz shows the saved map. The robot doesn't know where it is yet, so the **Navigation 2** panel
   shows `unknown`.

4. Click **2D Pose Estimate** in the toolbar.

![Click 2D Pose Estimate.](yt:81-9q7QfkHs@4:20)

5. Click and hold at the robot's *current* location on the map, drag in the direction it faces,
   and release.

![Click at the robot's location and drag to match its orientation.](yt:81-9q7QfkHs@4:28)

6. A cloud of green arrows appears: the robot's guesses of its position. It tightens as the robot
   drives and matches LiDAR readings to the map. The robot is ready.

![The green particle cloud shows the estimated position.](yt:81-9q7QfkHs@4:32)

7. Set a destination with **Nav2 Goal**, as before.

8. The **Navigation 2** panel shows whether navigation and localization are `active`, the ETA,
   remaining distance, time taken and number of recoveries.

![The Navigation 2 panel shows navigation status.](yt:81-9q7QfkHs@4:50#crop=0,0.08,0.3,0.5)

## Shut down

1. Press Ctrl-C in each window.

2. Type `exit` in the top window to stop the Docker container. It was started with `--rm`, so it is
   removed; your map is safe in `c:\maps`.

3. Close PowerShell.

## If navigation fails: "Goal Failed" errors

**Goal Failed** means the robot found no safe path to your goal. Usually obstacles are too close
together. The robot wants plenty of space around itself: if the path passes too close to an
obstacle, even without touching it, the robot refuses to drive.

To fix it:

- Make a clean map. If it is skewed or messy, map again, driving slowly.
- Remove obstacles.
- Leave plenty of space between the remaining ones.

![A nice, clean map.](https://makerspet.com/wp-content/uploads/2026/04/clean_map.webp)

!!! warning
    Navigation also fails if your PC is too slow. Watch for errors like
    `Transform data too old when converting from odom to map`: processing odometry took too long.
    Close other heavy programs, or use a faster PC.

## Tuning navigation

To tune mapping and navigation, edit `navigation.yaml`. Inside the container it is here:

```
/ros_ws/src/makerspet_mini/config/navigation.yaml
```

Tuning takes experimentation; search for "ROS2 Nav2 tuning" for tutorials. The settings you will
most likely change:

- **Speed.** The Nav2 controller, not teleop, sets autonomous speed. In `controller_server`, under
  `FollowPath`:
  - `max_vel_x`: top forward speed in m/s (default 0.22). Raise it gradually, for example to
    0.30, and set `max_speed_xy` to the same value.
  - `max_vel_theta`: top turning speed in rad/s (default 1.0).
  - `acc_lim_x` and `acc_lim_theta`: optionally reach target speed quicker.
- **Inflation radius.** How far the robot keeps from obstacles. Larger is safer but causes more
  "Goal Failed" errors in tight spaces.

!!! warning
    Keep `max_vel_x` comfortably below 0.4 m/s, the drivetrain's mechanical limit (200 RPM motor,
    derated 90%). Higher speed also gives the planner less time to react, so raise values in small
    steps and test each change.

Restart the navigation launch (Ctrl-C, then launch again) to apply changes. The `--rm` container
loses your edits when it stops; to keep them, commit it to your image from a Windows command
window before you exit:

```
docker container commit makerspet kaiaai/kaiaai:iron
# or, if you run the Jazzy image:
docker container commit makerspet kaiaai/kaiaai:jazzy
```

!!! tip
    Found better values than the `navigation.yaml` defaults? Please share them in the Maker's Pet
    support forum.

!!! note "Running more than one robot"
    Start one Docker container per robot, each with a unique `--name` and host UDP port, and point
    each robot's WiFi configuration at its port. For example (other options as above):

    ```
    docker run --name makerspet1 ... -p 8888:8888/udp ... kaiaai/kaiaai:iron
    docker run --name makerspet2 ... -p 8889:8888/udp ... kaiaai/kaiaai:iron
    ```

    Then open a shell with `docker exec -it makerspet1 bash` or `docker exec -it makerspet2 bash`.
