# 7. Using an Ubuntu PC Instead

Video: [Arduino/ROS2 self driving robot - Ubuntu software setup and robot bring up](https://youtu.be/fHPyjVdTNg4)
{: .video-link }

This chapter repeats Chapters 2 and 3 on a PC running **Ubuntu 22.04**. The differences: you give
your user access to serial ports, install two Python pieces the ESP32 uploader needs, use Docker
Engine instead of Docker Desktop, and share your X11 display with the container instead of running
an X server. Steps that match Windows are kept short and point back to Chapter 3.

Allow about an hour, plus download time for the Docker image. You need the assembled robot, a
USB cable for the ESP32 and a 2.4 GHz WiFi network.

![Software install and bring-up on Ubuntu 22.04.](yt:fHPyjVdTNg4@0:21)

## Install the Arduino IDE 1.8.19

1. On arduino.cc, click **Software**, scroll to **Legacy IDE (1.8.X)** and download **Arduino IDE
   1.8.19** for **Linux 64 bits**. (**Just download** skips the donation.)

   ![Download the Legacy IDE 1.8.19 for 64-bit Linux.](yt:fHPyjVdTNg4@0:38)

2. Open a terminal: click the **Apps** grid, type `terminal`, right-click the Terminal icon and
   choose **Add to Favorites**.
3. Unpack the archive (press **Tab** to complete file names):

    ```bash
    cd ~/Downloads
    ls
    tar -xvf arduino-1.8.19-linux64.tar.xz
    ```

   ![Unpacking the Arduino archive.](yt:fHPyjVdTNg4@1:18.5#crop=0.2,0.38,0.6,0.2)

4. Run the install script. It asks for your password because it installs system-wide:

    ```bash
    cd arduino-1.8.19/
    sudo ./install.sh
    ```

   ![The install script finishes with "done!".](yt:fHPyjVdTNg4@2:39#crop=0.2,0.42,0.8,0.46)

5. In **Apps**, add **Arduino IDE** to Favorites and launch it.

## Add the ESP32 toolchain

Same as Chapter 3.

1. In **File → Preferences**, paste this into **Additional Boards Manager URLs**:

    ```
    https://espressif.github.io/arduino-esp32/package_esp32_index.json
    ```

   ![Adding the Espressif boards URL.](yt:fHPyjVdTNg4@1:58)

2. In **Tools → Board → Boards Manager**, set **Type** to **Contributed**, find **esp32 by
   Espressif Systems**, select **2.0.17** and click **Install**.

   ![Install esp32 version 2.0.17.](yt:fHPyjVdTNg4@2:12)

3. Select **Tools → Board → ESP32 Arduino → ESP32 Dev Module**.

   ![Choose ESP32 Dev Module.](yt:fHPyjVdTNg4@2:25)

!!! update "Since the video was recorded"
    Stay on ESP32 board package **2.0.17**. In 2.0.15 HardwareSerial is broken: the firmware
    compiles but the LiDAR returns no data. 3.x removed `ledcAttachPin`/`ledcSetup`, which the
    firmware needs.

## Give yourself access to serial ports and install pyserial

On Ubuntu, only members of the `dialout` group can open serial ports, and the ESP32 uploader
(`esptool.py`) needs two Python fixes.

1. Add your user to `dialout` (in the video, `YOUR_USERNAME` is `ilia`):

    ```bash
    sudo usermod -a -G dialout YOUR_USERNAME
    ```

2. **Reboot your PC** so the group membership takes effect.

3. Install pip and the Python serial library:

    ```bash
    sudo apt install -y python3-pip
    pip3 install pyserial
    ```

   ![pyserial installed.](yt:fHPyjVdTNg4@3:05#crop=0.28,0.35,0.66,0.47)

   Ignore the warning that `pyserial-miniterm` and `pyserial-ports` are not on your PATH; the
   Arduino IDE doesn't use them.

!!! tip "Upload fails with \"No module named 'serial'\""
    Without pyserial, the upload ends with `ModuleNotFoundError: No module named 'serial'` and
    `Error compiling for board ESP32 Dev Module.` Run the two commands above and upload again.

## Download the firmware and copy it into the sketchbook

1. On [github.com/kaiaai/firmware](https://github.com/kaiaai/firmware), click **Releases**, expand
   **Assets** under the latest release and download **Source code (tar.gz)**.

   ![Download the latest firmware release.](yt:fHPyjVdTNg4@3:21)

2. Unpack it and copy its contents into your sketchbook, `~/Arduino`. The video uses release
   0.8.4; use your file's version number:

    ```bash
    cd ~/Downloads
    ls
    tar -xvf firmware-0.8.4.tar.gz
    cd firmware-0.8.4/
    cp -r * ~/Arduino/
    cd ~/Arduino/
    ls
    ```

   `ls` should list `kaiaai-esp32` (the sketch), `libraries`, `LICENSE`, `README.md` and `tools`.
   `tools` contains the **ESP32FS** plugin for **ESP32 Sketch Data Upload**, so unlike on Windows
   you don't install a separate SPIFFS plugin.

3. The ESP32 upload tools call `python`, but Ubuntu 22.04 only has `python3`. Link them:

    ```bash
    sudo ln -s /usr/bin/python3 /usr/bin/python
    ```

   ![Firmware copied and the python link created.](yt:fHPyjVdTNg4@3:57#crop=0.28,0.38,0.66,0.44)

!!! tip
    `ln: failed to create symbolic link '/usr/bin/python': File exists` means the link is already
    there (for example, from `python-is-python3`); skip this step.

## Upload the firmware

1. Restart the Arduino IDE so it picks up the new libraries and ESP32FS.
2. Open `~/Arduino/kaiaai-esp32/kaiaai-esp32.ino` (**File → Open**).
3. **Before** plugging in the robot, note the ports in **Tools → Port**. On my PC there is only
   `/dev/ttyS0`, a built-in serial port.

   ![Before plugging in, only /dev/ttyS0 is listed.](yt:fHPyjVdTNg4@4:23)

4. Plug in the ESP32 with the robot's power switch **OFF**.
5. In **Tools → Port**, select the new port, usually `/dev/ttyUSB0`.

   ![Select /dev/ttyUSB0.](yt:fHPyjVdTNg4@4:39)

   !!! tip
       Or run `ls /dev/ttyUSB*` before and after plugging in; the new entry is your robot.

6. Click **Upload**. When the output shows `Connecting....`, hold **BOOT** for 3–5 seconds.

   ![Hold BOOT for 3–5 seconds while the IDE connects.](yt:fHPyjVdTNg4@4:50)

## Upload the configuration data

The sketch's `data` folder holds YAML files describing the board's ESP32 pins and the robot's
properties (base and wheel diameter, wheel spacing, motor type, encoder pulses and more).

1. Press **Ctrl+K** (**Sketch → Show Sketch Folder**) and open the `data` folder.
2. Keep the YAML file for your board and robot and delete the other `config*.yaml` files. For the
   BLD-120MM-PACK (Mini body, BDC-30P board), keep `config_mini_bdc_30p.yaml`.

   ![Keep config_mini_bdc_30p.yaml.](yt:fHPyjVdTNg4@5:12)

3. Rename it to `config.yaml`.

   ![Rename it to config.yaml.](yt:fHPyjVdTNg4@5:22)

4. Unplug the ESP32 and plug it back in.
5. Choose **Tools → ESP32 Sketch Data Upload** and hold **BOOT** for 3–5 seconds as it connects.

   ![Tools → ESP32 Sketch Data Upload.](yt:fHPyjVdTNg4@5:41)

6. When it finishes, unplug and replug the ESP32.

!!! update "SPIFFS upload fails on Ubuntu"
    The Ubuntu SPIFFS plugin sometimes builds the image (`[SPIFFS] upload : /tmp/.../kaiaai-esp32.spiffs.bin`)
    and then prints `SPIFFS Upload failed!` without trying the upload. If so, upload the data once
    from a Windows PC (Chapter 3), then keep using Ubuntu.

## Configure the robot's WiFi

1. Open **Tools → Serial Monitor** at **115200** baud. You should see the firmware version,
   `SPIFFS mounted successfully`, `/config.yaml found; loaded OK` and
   `Setting up WiFi KAIA.AI; browse to http://192.168.4.1`.
2. Copy your PC's IP address (note the capital `I`):

    ```bash
    hostname -I
    ```

   ![WiFi setup ready (top); the PC's IP address (bottom).](yt:fHPyjVdTNg4@6:21)

   !!! note
       If it prints several addresses (one may be Docker's), use your home network's, such as
       `192.168.1.x`.

3. Connect your PC to the **KAIA.AI** WiFi network.
4. Browse to `http://192.168.4.1`, enter your 2.4 GHz **SSID 2.4GHz** and **WiFi Password**, paste
   your PC's IP into **Local PC IPv4**, and click **Connect**.

   ![The Kaia.ai Robot Configurator page.](yt:fHPyjVdTNg4@6:51)

5. Reconnect your PC to your local WiFi.
6. In the Serial Monitor, the robot prints `Connecting to WiFi ...`; if it stays stuck, press
   **EN** (reset). Once connected, it loads `/network.yaml`, prints the board and LiDAR model, and
   repeats `Connecting to Micro-ROS agent 192.168.1.139 ...` with your PC's IP. That's expected:
   ROS2 isn't running yet.

   ![The robot joins your WiFi network.](yt:fHPyjVdTNg4@7:28)

## Install Docker Engine

1. Open Docker's [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) page.
2. Under **Install using the apt repository**, copy step 1 (*Set up Docker's apt repository*) and
   run it in your terminal. Copy it from Docker's page, since they update it.

   ![Copy step 1 from Docker's page.](yt:fHPyjVdTNg4@7:51)

3. Run step 2 (*Install the Docker packages*). At the time of the video it was:

    ```bash
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

   ![Installing the Docker packages.](yt:fHPyjVdTNg4@8:13#crop=0.28,0.35,0.66,0.47)

4. Test it; you should see **Hello from Docker!**:

    ```bash
    sudo docker run hello-world
    ```

   ![Docker installed.](yt:fHPyjVdTNg4@8:31#crop=0.28,0.35,0.66,0.47)

!!! note
    Every `docker` command here starts with `sudo`. To drop it, see Docker's
    [Linux post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).

## Download the robot software image

1. Keep [github.com/kaiaai/kaiaai](https://github.com/kaiaai/kaiaai) open at **Launch ROS2/Kaia.ai
   (Docker only)**; its `# Ubuntu` lines are the commands below.
2. Pull the image (several gigabytes):

    ```bash
    sudo docker pull kaiaai/kaiaai:iron
    ```

   ![Pulling kaiaai/kaiaai:iron.](yt:fHPyjVdTNg4@8:54)

## Install Terminator

**Terminator** splits one window into the three or four shells you'll need.

1. Install it:

    ```bash
    sudo apt install terminator
    ```

   ![Installing Terminator.](yt:fHPyjVdTNg4@9:13)

2. Add **Terminator** to Favorites and launch it.
3. Press **Ctrl+Shift+O** (or right-click, **Split Horizontally**) to split it into two panes.

   ![Ctrl+Shift+O splits the window.](yt:fHPyjVdTNg4@9:37)

## Launch the robot software

1. In the **top** pane, start the container (the Ubuntu version of Chapter 3's `docker run`):

    ```bash
    sudo docker run --name makerspet -it --rm -v ~/maps:/root/maps -p 8888:8888/udp -p 4430:4430/tcp -e DISPLAY -e QT_X11_NO_MITSHM=1 --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --volume="${XAUTHORITY}:/root/.Xauthority" kaiaai/kaiaai:iron
    ```

   Compared with Windows:

   - `-v ~/maps:/root/maps` stores maps in `~/maps` instead of `c:\maps`.
   - `-p 8888:8888/udp` is the robot's micro-ROS agent port; `-p 4430:4430/tcp` is the same extra
     port as on Windows.
   - `-e DISPLAY`, `-e QT_X11_NO_MITSHM=1` and the `/tmp/.X11-unix` and `${XAUTHORITY}` volumes let
     RViz draw on your desktop, so no X server is needed.

2. In the **bottom** pane, open a second shell in the container:

    ```bash
    sudo docker exec -it makerspet bash
    ```

   ![Both panes at the container prompt, root@...:/ros_ws#.](yt:fHPyjVdTNg4@10:17#crop=0.39,0.22,0.61,0.5)

## Bring up the robot

From here on, everything works as in Chapter 3.

1. In the top pane, start the bring-up:

    ```bash
    ros2 launch kaiaai_bringup physical.launch.py
    ```

   ![The micro-ROS agent starts on port 8888.](yt:fHPyjVdTNg4@10:23#crop=0.39,0.22,0.61,0.45)

2. Unplug the USB cable, mount the LiDAR if you removed it, and turn the robot **ON**.

3. The robot connects, the top pane prints telemetry and the LiDAR spins.

   ![The LiDAR spins once the robot connects.](yt:fHPyjVdTNg4@10:41)

   !!! note
       Occasional `1 message(s) lost` and `RESULT_CRC_ERROR` lines are lost WiFi packets and
       harmless. If they scroll constantly or RViz stalls, see "Frequent CRC errors" in Appendix B.

4. In the bottom pane, start keyboard teleoperation:

    ```bash
    ros2 run kaiaai_teleop teleop_keyboard
    ```

   **w** drives forward, **x** backs up, **a** and **d** turn left and right, **space** stops.

   ![Teleop in the bottom pane.](yt:fHPyjVdTNg4@10:53#crop=0.39,0.22,0.61,0.78)

## Visualize the robot

1. Right-click the top pane, choose **Split Horizontally**, and open another container shell:

    ```bash
    sudo docker exec -it makerspet bash
    ```

2. Launch the visualization:

    ```bash
    ros2 launch kaiaai_bringup monitor_robot.launch.py
    ```

   ![Three panes: bring-up, monitor and teleop.](yt:fHPyjVdTNg4@11:30#crop=0.39,0.2,0.61,0.8)

3. RViz shows the LiDAR scan and a red heading arrow. Drive from the teleop pane and watch the scan move.

   ![RViz while driving with d, a and space.](yt:fHPyjVdTNg4@11:44)

## Shut down

1. Close RViz.
2. Press **Ctrl+C** in each pane.
3. Type `exit` in the top pane. `--rm` removes the container and ends the other shells. Close
   Terminator.

   ![Ctrl+C in each pane, then exit in the top pane.](yt:fHPyjVdTNg4@12:14#crop=0.39,0.2,0.61,0.8)

Next time, just start the container, run `physical.launch.py` and turn the robot on. In the
following chapters, use this chapter's `sudo docker run` wherever they show the Windows one.

!!! tip "Mapping on Ubuntu"
    Maps saved to `/root/maps` in the container land in `~/maps` on your PC. For simulation, drop
    `-p 4430:4430/tcp`:

    ```bash
    sudo docker run --name makerspet -it --rm -v ~/maps:/root/maps -p 8888:8888/udp -e DISPLAY -e QT_X11_NO_MITSHM=1 --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --volume="${XAUTHORITY}:/root/.Xauthority" kaiaai/kaiaai:iron
    ```

## Alternatives

**ROS2 without Docker.** On Ubuntu 22.04, run
[`install_ros2_iron_ubuntu_22_04.sh`](https://github.com/kaiaai/install/blob/iron/ubuntu/install_ros2_iron_ubuntu_22_04.sh), then [`install_kaiaai_iron.sh`](https://github.com/kaiaai/install/blob/iron/ubuntu/install_kaiaai_iron.sh). Wherever this chapter runs
`sudo docker exec -it makerspet bash`, open an ordinary terminal instead.

**ROS2 Jazzy.** The Jazzy image, `kaiaai/kaiaai:jazzy`, starts on Linux with [`start_jazzy.sh`](https://github.com/kaiaai/install/blob/jazzy/docker/utils/start_jazzy.sh).
Without Docker, on Ubuntu 24.04, run [`install_ros2_jazzy_ubuntu_24_04.sh`](https://github.com/kaiaai/install/blob/jazzy/ubuntu/install_ros2_jazzy_ubuntu_24_04.sh), then
[`install_kaiaai_jazzy.sh`](https://github.com/kaiaai/install/blob/jazzy/ubuntu/install_kaiaai_jazzy.sh).

!!! warning "Jazzy image: add --ipc=host whenever you use --net=host"
    The Jazzy image passes ROS2 messages through shared memory, and `start_jazzy.sh` uses
    `--net=host`. In your own `docker run` with `--net=host`, add `--ipc=host`. Without it, ROS2
    nodes outside the container (on your PC or in another `--net=host` container) see its topics
    but receive no messages. Nodes inside the container, and the robot, work either way.

**Raspberry Pi and other ARM64 boards.** The Docker image is x86-64 only. Install Ubuntu 22.04 on
the Pi, run `install_ros2_iron_ubuntu_22_04.sh` (or the official ROS2 Iron Ubuntu .deb
instructions), then `install_kaiaai_iron.sh`. For Jazzy, use Ubuntu 24.04 with
`install_ros2_jazzy_ubuntu_24_04.sh` and `install_kaiaai_jazzy.sh`.

**Ubuntu in a virtual machine on Windows.** If WSL2 doesn't work, you can follow this chapter in an
Ubuntu 22.04 VM. I don't recommend it: in my experience the VM makes ROS2 laggy. You can also upload
the firmware from Windows (Chapter 3) and run only ROS2 in the VM.

!!! draft "Question for Ilia"
    Scripts link to github.com/kaiaai/install, as in the guide. Should the book also give the exact
    commands to run them (e.g. `bash install_ros2_iron_ubuntu_22_04.sh`)?
