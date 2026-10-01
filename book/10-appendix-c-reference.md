# Appendix C. Quick Reference

## Start the robot software

**Windows (PowerShell).** Start Docker Desktop and the X server (XLaunch, display number 0) first.

```
docker run --name makerspet -it --rm -v c:\maps:/root/maps -p 8888:8888/udp -p 4430:4430/tcp -e DISPLAY=host.docker.internal:0.0 -e LIBGL_ALWAYS_INDIRECT=0 kaiaai/kaiaai:iron
```

**Ubuntu (terminal).**

```
sudo docker run --name makerspet -it --rm -v ~/maps:/root/maps -p 8888:8888/udp -p 4430:4430/tcp -e DISPLAY -e QT_X11_NO_MITSHM=1 --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --volume="${XAUTHORITY}:/root/.Xauthority" kaiaai/kaiaai:iron
```

**Open another shell in the running container** (on Ubuntu, prefix with `sudo`):

```
docker exec -it makerspet bash
```

**Stop a container that is still running** (e.g. after closing a window without `exit`):

```
docker container stop makerspet
```

**Keep changes you made inside the container:**

```
docker container commit makerspet kaiaai/kaiaai:iron
```

## ROS 2 commands (inside the container)

| Task | Command |
|---|---|
| Connect to the physical robot | `ros2 launch kaiaai_bringup physical.launch.py` |
| Drive with the keyboard | `ros2 run kaiaai_teleop teleop_keyboard` |
| View the LiDAR scan in RViz | `ros2 launch kaiaai_bringup monitor_robot.launch.py` |
| Map while driving (SLAM + Nav2) | `ros2 launch kaiaai_bringup navigation.launch.py slam:=True` |
| Explore automatically | `ros2 launch explore_lite explore.launch.py` |
| Save the map | `ros2 run nav2_map_server map_saver_cli -f ~/maps/map --ros-args -p save_map_timeout:=60.0` |
| Navigate on a saved map | `ros2 launch kaiaai_bringup navigation.launch.py map:=$HOME/maps/map.yaml` |
| Start the simulation (Gazebo) | `ros2 launch kaiaai_gazebo world.launch.py` |
| Map in simulation | `ros2 launch kaiaai_bringup navigation.launch.py use_sim_time:=true slam:=True` |
| Read a robot parameter | `ros2 param get /pet motor.encoder.ppr` |

More commands are in the command cheat sheets at
[github.com/kaiaai/kaiaai](https://github.com/kaiaai/kaiaai); the container prints this link when it starts.

## Teleop keys

| Key | Action |
|---|---|
| `w` / `x` | Increase / decrease forward speed (keep pressing `x` to reverse) |
| `a` / `d` | Turn left / right faster |
| `s` | Stop turning, keep going straight |
| `Space` | Stop |
| `Ctrl-C` | Quit |

## ESP32 activity LED

| LED | Meaning |
|---|---|
| Solid on | WiFi configuration (AP) mode: connect to the `KAIA.AI` network and browse to http://192.168.4.1 |
| Slow blink, once per second | Connecting to WiFi |
| Very slow blink, once per 20 seconds | Connected to WiFi, connecting to the ROS 2 PC |
| Fast blink | Connected to the ROS 2 PC |

**Reset the WiFi settings:** press and release the ESP32 reset (EN) button, then within one second
press and hold BOOT until the LED turns solid on. Release BOOT; the ESP32 restarts in WiFi
configuration mode.

## Versions used in this book

| Item | Version |
|---|---|
| Arduino IDE | 1.8.19 (recommended) or 2.x |
| ESP32 board package (esp32 by Espressif) | 2.0.17; avoid 2.0.15 and 3.x |
| Robot firmware | Kaia.ai 0.8.x (`-iron`) |
| ROS 2 | Iron, Docker image `kaiaai/kaiaai:iron` (Jazzy: `kaiaai/kaiaai:jazzy`) |
| PC operating system | Windows 10/11 with WSL2, or Ubuntu 22.04 |

## Links

**Instructions and help**

- Video course playlist: [youtube.com/playlist?list=PLOSXKDW70aR8uA1IFahSKVuk5ODDfjTZV](https://www.youtube.com/playlist?list=PLOSXKDW70aR8uA1IFahSKVuk5ODDfjTZV)
- Up-to-date build guide and FAQ: [makerspet.com/blog/bld-120mm-pack](https://makerspet.com/blog/bld-120mm-pack/)
- Simulation tutorial: [makerspet.com/blog/tutorial-map-navigate-ros2-robot-in-simulation](https://makerspet.com/blog/tutorial-map-navigate-ros2-robot-in-simulation/)
- Support forum: [github.com/makerspet/support/discussions](https://github.com/makerspet/support/discussions)
- Discord: [discord.gg/3y2JKz5T25](https://discord.gg/3y2JKz5T25)

**Software and configuration**

- Robot firmware: [github.com/kaiaai/firmware](https://github.com/kaiaai/firmware)
- ROS 2 packages and command cheat sheets: [github.com/kaiaai/kaiaai](https://github.com/kaiaai/kaiaai)
- Robot model, navigation and teleop settings: [github.com/makerspet/makerspet_mini](https://github.com/makerspet/makerspet_mini/tree/iron/config)
- Default `config.yaml` (BDC-30P): [github.com/kaiaai/firmware/.../data/config.yaml](https://github.com/kaiaai/firmware/blob/iron/kaiaai-esp32/data/config.yaml)
- Configuration file reference: [blog.kaia.ai/kaiaai-configuration-file](https://blog.kaia.ai/kaiaai-configuration-file)
- Native install scripts (no Docker): [github.com/kaiaai/install](https://github.com/kaiaai/install)

**Other LiDARs**

- [YDLIDAR X3, X3PRO, X2, X2L, X4 and SCL](https://makerspet.com/blog/connect-ydlidar-x3-to-makerspet-esp32-boards/)
- [Delta-2A, 2B and 2G](https://makerspet.com/blog/connect-delta-2g-lidar-to-makerspet-esp32-boards/)
- [Xiaomi LDS02RR](https://makerspet.com/blog/how-to-connect-xiaomi-lds02rr-lidar-to-esp32/)

**3D printing**

The robot's plastic parts are open source. The build guide's "Download Files for 3D Printing"
section links the 3MF files for the base, LiDAR skirts, LiDAR posts, board posts, caster roller,
caster mounts, battery holder backstop, wheels and motor clamps, plus the full Autodesk Fusion 360
model. When printing the caster roller and wheels, set your slicer's seam position to **Random**.

!!! draft "Question for Ilia"
    The guide's 3MF and Fusion 360 links didn't survive the text extraction. Do you want direct URLs
    here, or is pointing to the guide page better (it stays current)?
