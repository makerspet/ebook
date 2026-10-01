# 3. Upload the Firmware and Bring Up the Robot

Video: [Step by Step Arduino LiDAR Robot Bringup](https://youtu.be/tKfVU1n5TjA)
{: .video-link }

You upload the firmware and its configuration ("sketch data") to the ESP32, connect the robot to
your WiFi and start the ROS2 software on your PC. At the end you drive the wheels from your keyboard
and see live LiDAR data.

You need the assembled robot (Chapter 1) and the PC software from Chapter 2. Plan for about
30 minutes.

## Upload the firmware (Arduino IDE 2.x)

1. In Arduino IDE 2.x, open the `kaiaai-esp32` sketch.
2. If the IDE offers library or board updates, click **LATER**. Newer versions can break the build.

   ![Close the update pop-ups. Don't update.](yt:tKfVU1n5TjA@0:36)

3. Connect the ESP32 to your PC over USB, with the board's power switch **off**.

   ![Plug the USB cable into the ESP32.](yt:tKfVU1n5TjA@0:42)

4. In the board selector, choose **DOIT ESP32 DEVKIT V1** and your COM port (`COM3` in the video).
   For a Maker's Pet ESP32-S3 driver board, choose **ESP32S3 Dev Module**.

   ![Select the board and COM port.](yt:tKfVU1n5TjA@0:52)

5. Click **Upload** (the right arrow). The first compile takes a while.
6. When the output shows `Connecting....`, press and hold **BOOT** for 3 to 5 seconds to put the
   ESP32 into download mode.

   ![Hold BOOT when the upload starts connecting.](yt:tKfVU1n5TjA@1:02)

!!! update "Since the video was recorded"
    Some ESP32 boards don't need BOOT pressed; if the upload succeeds without it, that's fine. If it
    fails with `Failed to connect to ESP32: No serial data received`, retry and press BOOT as soon as
    `Connecting...` appears.

7. Wait for `Hash of data verified.` and `Hard resetting via RTS pin...`.
8. Open **Tools → Serial Monitor** at **115200 baud** and press the ESP32's **EN** (reset) button.
9. The ESP32 boots and asks for sketch data, as expected:

   ```
   Kaia.ai firmware version 0.8.0-iron
   ESP IDF version v4.4.7-dirty
   SPIFFS mounted successfully
   Sketch data not found. Please upload sketch data.
   ```

   ![The ESP32 asks for sketch data.](yt:tKfVU1n5TjA@1:27#crop=0.36,0.40,0.50,0.47)

!!! note
    Some 38-pin ESP32 boards print `E (43) SPIFFS: mount failed, -10025` instead. It means the same
    thing.

## Upload the sketch data (Arduino IDE 2.x)

The sketch data is the robot's configuration file, `config.yaml`, plus the WiFi setup web page. It
lives in a separate flash area (SPIFFS), so it is uploaded separately.

1. **Close the Serial Monitor**; it holds the COM port and the upload will fail.
2. Open **Sketch → Show Sketch Folder** and go into the `data` folder.
3. It has one config file per hardware option. In the video:

   ```
   config.yaml
   config_mini_32e.yaml
   config_mini_bdc_30p.yaml
   config_mini_bdc_38c4.yaml
   config_mini_esp32s3_devkitc_1.yaml
   config_mini_s3m.yaml
   favicon.png
   index.html
   ```

   ![The data folder.](yt:tKfVU1n5TjA@1:38#crop=0.1,0.37,0.68,0.5)

4. Delete every `.yaml` file **except** the one for your hardware: `config_mini_bdc_30p.yaml` for the
   BLD-120MM-PACK with the BDC-30P board. Keep `favicon.png` and `index.html`.
5. Rename the file you kept to `config.yaml`. It sets the ESP32 pins, motors and LiDAR model.

   <div class="pair" markdown="1">
   ![Keep only your board's config…](yt:tKfVU1n5TjA@1:44)
   ![…and rename it to config.yaml.](yt:tKfVU1n5TjA@1:47)
   </div>

!!! draft "Question for Ilia"
    The video uses `config_mini_bdc_30p.yaml` from the firmware's data folder (overlay at 1:44).
    The guide links "config.yaml for BLD-120MM-PACK with a BDC-30P driver board" to
    [makerspet/store/.../MINI-BDC30P-BODY/v1.0.0/config_bdc_30p.yaml](https://github.com/makerspet/store/blob/main/MINI-BDC30P-BODY/v1.0.0/config_bdc_30p.yaml).
    Which should readers use? If the store file, this step becomes an `!!! update`: download it,
    rename it to config.yaml, put it in the data folder.

!!! warning "Pick the config for your exact ESP32 chip"
    The BDC-30P takes an ESP32 DOIT DevKit v1 (plain ESP32, not ESP32-S3). An ESP32-S3 config on a
    plain ESP32, or vice versa, uses the wrong GPIO for the reset button, so the firmware thinks it
    is always pressed and keeps booting into WiFi configuration (AP) mode.

6. Click inside the code window, press **Ctrl+Shift+P**, type `Upload` and click
   **Upload SPIFFS to Pico/ESP8266/ESP32**.

   ![Pick Upload SPIFFS to Pico/ESP8266/ESP32.](yt:tKfVU1n5TjA@2:08#crop=0.19,0.08,0.54,0.44)

7. If it fails right away with `ERROR: No port specified, check IDE menus.`, restart the IDE and
   retry. This happens often.

   ![A common SPIFFS upload error.](yt:tKfVU1n5TjA@1:56#crop=0.36,0.40,0.50,0.16)

8. At `Connecting....`, hold **BOOT** for 3 to 5 seconds.

!!! tip "If the SPIFFS upload still fails"
    - `Could not open COM3, the port doesn't exist`: close the Serial Monitor, check the USB cable,
      retry.
    - `SPIFFS_write error(-10010): unknown` / `error adding file!`: a file name in `data` is over
      30 characters.
    - `This chip is ESP32-S3 not ESP32. Wrong --chip argument?`: wrong board selected in the IDE.

    See Appendix B for more.

9. Close the SPIFFS Upload output tab, reopen the Serial Monitor and press **EN**.
10. The ESP32 loads `config.yaml` and enters WiFi configuration mode:

    ```
    SPIFFS mounted successfully
    /config.yaml found; loaded OK
    WiFi SSID unknown
    dest_ip unknown
    To enter web config push-and-release EN, then push-and-hold BOOT within 1 sec
    Setting up WiFi KAIA.AI; browse to http://192.168.4.1
    ```

    ![Config loaded; ready for WiFi configuration.](yt:tKfVU1n5TjA@2:34#crop=0.36,0.40,0.50,0.47)

## If you use the legacy Arduino IDE 1.8.19

Only the menus differ. Do the `data` folder config-file steps before step 8.

1. Open the robot's sketch in Arduino IDE 1.8.19.
2. Select **Tools → Board → ESP32 Arduino → ESP32 Dev Module** (**ESP32S3 Dev Module** for Maker's
   Pet ESP32-S3 boards).

   ![In IDE 1.8.19, choose ESP32 Dev Module.](yt:tKfVU1n5TjA@2:46)

3. Connect the ESP32 over USB with the power switch off.
4. Select your COM port under **Tools → Port** and click **Upload**.
5. Hold **BOOT** for 3 to 5 seconds when the upload starts connecting.
6. Open **Tools → Serial Monitor** and press **EN**. The ESP32 asks for sketch data.
7. Close the Serial Monitor.
8. Run **Tools → ESP32 Sketch Data Upload** and hold **BOOT** for 3 to 5 seconds when it connects.

   ![The sketch data upload is in the Tools menu.](yt:tKfVU1n5TjA@3:33)

9. Reopen the Serial Monitor and press **EN**. The ESP32 loads `config.yaml` and enters WiFi
   configuration mode.

## Configure the robot's WiFi

In configuration (AP) mode the ESP32 creates its own hotspot, `KAIA.AI`. Connect to it and use a web
page to give the robot your WiFi name and password and your PC's IP address, where the ROS2
software runs.

1. The ESP32's blue activity LED is **solid on** in AP mode.

   ![Activity LED solid on: AP mode.](yt:tKfVU1n5TjA@4:04)

   | Activity LED | What the robot is doing |
   |---|---|
   | Solid on | AP mode, waiting for WiFi configuration |
   | Slow blinking, once per second | Connecting to your WiFi |
   | Very slow blinking, once per 20 seconds | Connected to WiFi, connecting to the ROS2 PC |
   | Fast blinking | Connected to the ROS2 PC |

2. On your PC, in PowerShell or `cmd.exe`, run:

   ```
   ipconfig
   ```

3. Note the **IPv4 Address** under **Wireless LAN adapter Wi-Fi** (`192.168.1.113` in the video),
   not a VMware or other virtual adapter.

   ![Note the Wi-Fi adapter's IPv4 Address.](yt:tKfVU1n5TjA@4:22#crop=0.08,0.15,0.72,0.66)

4. Connect your PC to the open **KAIA.AI** network.

   ![Connect to KAIA.AI.](yt:tKfVU1n5TjA@4:34)

5. Browse to `http://192.168.4.1` to open the **Kaia.ai Robot Configurator**.

   ![The Kaia.ai Robot Configurator.](yt:tKfVU1n5TjA@4:50#crop=0,0,0.95,0.5)

6. Enter your WiFi name in **SSID 2.4GHz** and its password in **WiFi Password**.
7. Enter your PC's IPv4 address from step 3 in **Local PC IPv4** and click **Connect**.

   ![Fill in WiFi and PC IP, then click Connect.](yt:tKfVU1n5TjA@5:06)

!!! warning "2.4 GHz WiFi only"
    The ESP32 can't use 5 GHz. If your router has separate network names, enter the 2.4 GHz one
    (`NETGEAR48`, not `NETGEAR48_5G`, in the video).

8. The page shows **Connecting to WiFi...** with the saved settings (`dest_port 8888` is the port the
   robot uses to reach your PC). The robot saves them to `/network.yaml`, restarts and joins your
   WiFi:

   ```
   /network.yaml found; loaded OK
   /config.yaml found; loaded OK
   Board model MINI-BDC30P-BODY with BDC-30P, version v1.1.1, manufacturer makerspet.com
   LIDAR model LDROBOT LD14P
   Motor driver type IN1_IN2; motor encoder type AB_QUAD
   Connecting to WiFi NETGEAR48 ... connected, IP 192.168.93.127
   ```

   ![The robot restarted and joined your WiFi.](yt:tKfVU1n5TjA@5:12)

9. Reconnect your PC to your WiFi; it may not switch back on its own.

!!! note "If your PC's IP address changes"
    For example after a router restart, the robot joins WiFi but can't find the PC. Reset the
    robot's WiFi settings (end of this chapter) and enter the new address.

## Launch the robot software on your PC

1. Make sure Docker Desktop is running.

   ![Docker Desktop must be running.](yt:tKfVU1n5TjA@5:30)

2. Make sure your X server is running; it shows the robot software's windows (RViz) on your
   desktop. In the video it's VcXsrv, started with XLaunch: set **Display number** to `0`, then
   click **Next** through to **Finish**.

   ![In XLaunch, set Display number to 0.](yt:tKfVU1n5TjA@5:37#crop=0.07,0.12,0.37,0.52)

3. Open Windows PowerShell and start the robot software container:

   ```
   docker run --name makerspet -it --rm -p 8888:8888/udp -p 4430:4430/tcp -e DISPLAY=host.docker.internal:0.0 -e LIBGL_ALWAYS_INDIRECT=0 kaiaai/kaiaai:iron
   ```

   ![Start the kaiaai/kaiaai:iron container.](yt:tKfVU1n5TjA@5:54)

   The prompt changes to something like `root@6028bbee19de:/ros_ws#`: a Linux shell inside the
   container. The robot talks to the PC on port 8888/udp, hence `dest_port 8888`.

!!! tip "If docker run fails"
    - `error during connect: ... dockerDesktopLinuxEngine ...`: launch Docker Desktop.
    - `Conflict. The container name "/makerspet" is already in use`: your last session's container
      is still running. Run `docker container stop makerspet` and retry. Next time, leave each shell
      with `exit` instead of closing the window.
    - `Ports are not available: exposing port TCP 0.0.0.0:4430`: reboot your PC.

## Bring up the robot and test the motors

1. Open the Arduino Serial Monitor to watch the robot's messages.
2. Put the robot on a pedestal, such as a small box, so the wheels spin freely.

   ![Wheels in the air.](yt:tKfVU1n5TjA@6:10)

3. Turn the power switch **on** and press **EN**. The robot joins your WiFi and tries to reach your
   PC (`Connecting to Micro-ROS agent 192.168.1.113 ...`). If WiFi fails, press **EN** again.
4. In the container shell, run:

   ```
   ros2 launch kaiaai_bringup physical.launch.py
   ```

   ![Run the physical robot launch.](yt:tKfVU1n5TjA@6:26)

5. The robot connects, and the Serial Monitor prints periodic status:

   ```
   Connecting to Micro-ROS agent 192.168.1.113 ... success
   Syncing time ... OK
   micro-ROS client key 0x8B6C9A69; ROS2 node /pet
   Micro-ROS initialized
   LiDAR info Model: LDROBOT LD14P
   startLIDAR() result: OK
   Telem avg 24 max 27ms, LiDAR RPM 5.01, wheels RPM 0.00 0.00, battery 8.14V, RSSI -62dBm
   ```

   ![The ESP32 has connected to ROS2.](yt:tKfVU1n5TjA@6:29)

6. The activity LED now blinks rapidly.

!!! tip "Read the status line"
    `Telem` shows LiDAR speed, wheel speeds, battery voltage and WiFi signal (RSSI). **LiDAR RPM
    must not be zero.** If it stays `0.00`, check the LiDAR wires and that `config.yaml` matches your
    LiDAR (LD14P by default).

!!! tip "Connected to WiFi, but not to the PC?"
    If `Connecting to Micro-ROS agent ...` repeats without `success`:
    - Check that `physical.launch.py` is running in the container.
    - Check the robot and PC are on the same network, and it doesn't block devices from talking to
      each other ("client isolation"), as café, restaurant and university networks often do.
    - Check your PC's IP address hasn't changed.
    - Make sure your PC accepts incoming local connections. Try disabling your antivirus: my
      Avast started blocking these ports in December 2025.

    See Appendix B for more.

7. In Windows Terminal, hold **Alt** and click **+** to split the window into a second PowerShell
   pane.
8. Click inside it and open another shell in the running container:

   ```
   docker exec -it makerspet bash
   ```

9. Run the teleoperation app:

   ```
   ros2 run kaiaai_teleop teleop_keyboard
   ```

   ![A second shell in the container runs teleop_keyboard.](yt:tKfVU1n5TjA@6:54#crop=0.49,0.52,0.51,0.38)

10. With the teleop pane selected, drive the wheels:
    - Press **w** repeatedly to speed up forward to maximum. Watch the wheel RPM rise in the
      Serial Monitor.
    - Press **x** several times to slow down and reverse.
    - Press **space** to stop, then **d** to spin right.
    - Press **space** to stop, then **a** to spin left.
    - Press **space** to stop.

    ![The wheels at maximum speed.](yt:tKfVU1n5TjA@7:12)

If both wheels turn the right way, the motors work. If a wheel doesn't turn, turns the wrong way or
only runs at full speed, see Appendix B.

## Check the LiDAR

1. Turn the power off and unplug the USB cable.
2. Reattach the LiDAR if you removed it.

   ![Reattach the LiDAR.](yt:tKfVU1n5TjA@7:48)

3. Hold **Alt**, click **+** and click inside the new pane. Windows Terminal splits the selected
   pane; if one opens in the wrong place, type `exit` in it and retry.
4. Open another container shell and start the LiDAR visualization:

   ```
   docker exec -it makerspet bash
   ros2 launch kaiaai_bringup monitor_robot.launch.py
   ```

   ![A third shell opens RViz.](yt:tKfVU1n5TjA@8:14)

   An empty RViz window opens.

5. Turn the robot on. The white dots in RViz are what the LiDAR sees; the red arrow shows which way
   the robot faces.

   ![Live LiDAR scan in RViz.](yt:tKfVU1n5TjA@8:41)

!!! warning "RViz doesn't open?"
    `could not connect to display host.docker.internal:0.0` means your X server isn't running.
    Start it (display number 0) and rerun the command.

!!! note
    A few `RESULT_CRC_ERROR` and `message(s) lost` lines are normal. If they flood the terminal,
    WiFi packets are being dropped: move the robot and PC closer to the router and avoid heavy WiFi
    use.

## Shut down

1. Turn the robot off.
2. Press **Ctrl+C** in each shell.
3. Type `exit` in each shell. Exiting the `docker run` shell stops the container, and `--rm`
   removes it so the name is free next time.

Next, you'll map your place and make the robot self-drive around obstacles.

## Reset the robot's WiFi settings

To change the WiFi network or your PC's IP address:

1. Power up the ESP32 (USB or battery).
2. Press **EN**, then within 1 second press and hold **BOOT**. The LED blinks very fast.
3. Keep holding until the LED turns solid on.
4. Release **BOOT**. The ESP32 reboots into AP mode; configure WiFi again as above.

<div class="pair" markdown="1">
![Press EN, then hold BOOT.](yt:tKfVU1n5TjA@9:16)
![Release BOOT: WiFi configuration mode.](yt:tKfVU1n5TjA@9:24)
</div>

Full documentation and troubleshooting:
[makerspet.com/blog/bld-120mm-pack/](https://makerspet.com/blog/bld-120mm-pack/) and Appendix B.
