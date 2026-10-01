# Appendix B. Troubleshooting and FAQ

The most common problems, by symptom. The latest version is at
[makerspet.com/blog/bld-120mm-pack](https://makerspet.com/blog/bld-120mm-pack/).

Look for clues in two places:

- **The ESP32.** Connect it over USB, open the Arduino Serial Monitor at 115200 baud and press EN
  (reset). The firmware prints its configuration, connection progress and telemetry (see B.9).
- **ROS2.** Read the output in the shell where you launched it.

## B.1 Where to get help

If this appendix doesn't cover your problem, ask:

- On the support forum: [github.com/makerspet/support/discussions](https://github.com/makerspet/support/discussions).
- On the [Maker's Pet Discord server](https://discord.gg/3y2JKz5T25).

Include your Serial Monitor output, full ROS2 output, exact `docker run` command, system (Windows
with WSL, Ubuntu, a virtual machine) and wiring photos. For navigation problems, add a screen
recording of RViz and the terminal plus a phone video of the robot.

## B.2 Power and batteries

### Battery connected, but no power

- Check the board's ON/OFF switch.
- Check the battery wires are in the correct screw terminals and make good contact. Measure the
  voltage at the board's power terminals.
- Check the polarity. **Reversed polarity will burn the board.**
- Wiggle the batteries in the holder. Measure each battery, and the voltage at the holder terminals.
- Check the ESP32 power LED lights up with the switch ON.

### Can I use 18650 Li-Ion batteries instead of 6×AA?

The BDC-30P (and BDC-38C4) boards are designed for alkaline batteries and have **no on-board
protection** for rechargeable cells. If you still use them, the 120 mm base fits a 2-cell 18650
holder:

- Use **protected** cells in series (short circuit, overcurrent, overcharge, overdischarge and so on).
- Take the cells out to charge them in your own charger.
- The robot draws up to around 3 A continuous and around 5 A peak; typical consumption is much
  lower (see [Power consumption](#power-consumption)).

Mount the rear posts in the outer spare holes of the base, fit the battery-holder backstop behind
the battery with two M3 countersunk screws, and use the wider LiDAR skirt that matches the rear
post positions.

!!! warning
    Using rechargeable batteries is at your own risk.

!!! draft "Question for Ilia"
    Forum [#106](https://github.com/makerspet/support/discussions/106) (September 2026) reports the
    2×18650 holder hits the LiDAR posts on a self-printed chassis STL v1.0.1. Add a chassis variant
    or note?

### What battery voltage drives the motors? (Vbat, Vmot, JP2)

The board steps the battery voltage (Vbat) **up** to the motor voltage (Vmot), with about 2 V of
headroom:

- For 12 V Vmot (JP2 closed, the default), Vbat must be about 6–10 V. A 3S LiPo (11.1 V) will not
  work reliably; use a 2S pack (about 7.4 V).
- For 24 V Vmot (JP2 open), Vbat may be about 6–21 V.

JP2 selects the Vmot output; it does not pass raw battery voltage to the motors.

### Power consumption

Measured with a 9 V battery, the ESP32 connected to the ROS2 PC over WiFi (USB unplugged), an
LDROBOT LD14P LiDAR running and two 12 V N20 motors, firmware 0.8.0-iron:

| Condition | Battery current |
|---|---|
| Both motors off | about 240 mA |
| Both motors full on, spinning freely | about 430–450 mA |

## B.3 Motors and encoders

### A motor doesn't turn, or behaves strangely

Start with the mechanics and wiring:

- Make sure the board's post tab doesn't touch a motor (see the figure). A blocked motor can burn
  out.
- Check the switch is ON and the batteries are connected and fresh.
- **Double-check the motor connections**, the most common issue:
    - The motor's connector housing can slide up, off its pins. Press it back down fully.
    - Make sure the motor wires go to the correct screw terminals.
    - A screw terminal wire can break off or fail to make contact. Follow Chapter 1 for reliable
      connections.
- Check the green LED on each motor. Off means the encoder has no power: check the battery, switch
  and cable connections at both ends.
- Keep debris out of the gearbox; it can seize the gears and burn out the motor.
- Don't overtighten the motor screws. Bent plastic (including the base) can catch the gears or the
  encoder disk and burn out the motor.
- Gently spin the magnet. If the core shaft spins freely, the gearbox may be seizing.
- Bent encoder sensors can touch the encoder wheel. Bend them back and check the magnet spins
  freely.

![The post tab must not touch the motor, as it does here.](https://makerspet.com/wp-content/uploads/2026/04/pcb_post_touches_motor.webp)

Then test: start teleop in ROS2 and press **W** to turn the motors forward.

### A motor does not move at all

- Check for cables blocking the encoder magnet.
- Check that neither motor is mechanically stalled.
- Check that the M1 and M2 wires are firmly connected to the board.
- Check that the batteries are fresh.

### One motor works, the other doesn't

Swap the two motors (see Chapter 1). If the problem follows the motor, the motor or its cable is at
fault; if it stays on the same side, check that side's board connections.

### A motor spins at full speed in one direction no matter what you command

Forward, backward and stop all give the same result.

- Swap the motor's ENCA and ENCB encoder wires.
- Check that both encoder wires are connected reliably.

### A motor spins only at full speed, but does change direction

An encoder wire probably has a bad connection, at the board or at the motor.

### Both motors turn at one fixed speed and pressing a key repeatedly doesn't change it

Usually motor wiring. Try swapping M+ and M−, and/or ENCA and ENCB
([forum #63](https://github.com/makerspet/support/discussions/63)).

### A motor turns the wrong way but otherwise responds correctly

Swap the motor's ENCA and ENCB wires, then swap its M1 and M2 wires.

### A motor turns unevenly

- Check for flaky wire connections.
- With third-party motors (not from Maker's Pet), you may need to tune the motor PID coefficients in
  `config.yaml`.

### Motor changes speed abruptly

Check the soldering on the motor's encoder board and resolder any loose components.

![Check the soldering on the N20 encoder board.](yt:jNF1pKFe9b8@0:02)

!!! draft "Question for Ilia"
    Which component is the defect here? The tweezers point at the black sensor next to the connector
    at 0:02. If you can name it (for example, "the Hall sensor"), the caption can say so.

### A motor runs at full speed at power-up, before WiFi connects

Some ESP32 motor-driver GPIOs float or go HIGH during boot or reset, spinning a motor at full speed
until the firmware takes control. It's not a wiring fault. Drive those pins LOW with
`digitalWrite(pin, LOW);` at the very start of `setup()`.

### My motor won't spin, change speed or stop (external motor driver)

With a separate motor driver board, the firmware PWMs the driver's IN1/IN2 inputs. TB6612FNG,
DRV8871, DRV8833, DRV8835 and L298N all work. Two things are required:

1. **Hold the driver's enable pins HIGH**, or the motor won't move. On a TB6612FNG, tie PWMA, PWMB
   and STBY high; on an L298N, ENA and ENB (with the on-board jumpers or to 5 V). Either wire them
   high, or add `digitalWrite(PWMA, HIGH);` (and so on) at the top of `setup()`.
2. **Set the driver type in `config.yaml`** (`IN1_IN2` for these drivers) and map each motor's
   GPIOs. If a wheel spins the wrong way or won't stop, swap that motor's `in1`/`in2`, or its
   encoder `a`/`b`.

See the [TB6612FNG worked example](https://makerspet.com/blog/connect-tb6612fng-motor-driver-to-esp32/),
the schematic below ([forum #24](https://github.com/makerspet/support/discussions/24)) and the
[configuration file reference](https://blog.kaia.ai/kaiaai-configuration-file). Pick any GPIOs
within the ESP32's limitations
([ESP32](https://makerspet.com/blog/esp32-gpio-limitations/),
[ESP32-S3](https://makerspet.com/blog/esp32-s3-gpio-limitations/)).
An L298N wired this way works with the unmodified firmware and `config.yaml`
([forum #77](https://github.com/makerspet/support/discussions/77)).

![TB6612FNG wiring to a 30-pin ESP32; the GPIO numbers are an example. From forum #24.](https://github.com/user-attachments/assets/0395445f-7f0d-4343-aa1d-14720904130f)

### Using a BLDC motor with a built-in controller (ESC-type, FG output)

Five-wire "ESC-type" BLDC motors have a built-in driver, so no external ESC is needed. In
`config.yaml`, set `motor.driver.type: PWM_CW` and `motor.encoder.type: FG`, then map each side's
FG, PWM and CW GPIOs.

- FG reports speed only, not direction; direction follows the CW/CCW input.
- The PID needs roughly 1000 PPR. A low-PPR FG signal makes low-speed control twitchy.

!!! warning
    A BLDC motor's PWM and CW inputs may be pulled up internally to 12 V or 24 V, which will damage
    the ESP32. Use a logic-level converter.

### Can I use an IMU (BNO055, MPU6050) instead of wheel encoders?

No. There's no built-in IMU support, and the motor PID needs encoders to control RPM. You can map
and navigate without odometry (an option in `navigation.yaml`), but not without encoders. IMU
streaming is possible but not trivial: the WiFi/UDP link drops some high-rate IMU packets.

## B.4 Arduino IDE: compile and upload

### Compilation fails with "This code runs on ESP32"

```
aiaai-esp32:16:4: error: #error This code runs on ESP32
   #error This code runs on ESP32
    ^~~~~
In file included from /home/ilia/Arduino/kaiaai-esp32/kaiaai-esp32.ino:19:0:
robot_config.h:16:10: fatal error: SPIFFS.h: No such file or directory
 #include <SPIFFS.h>
          ^~~~~~~~~~
compilation terminated.
exit status 1
#error This code runs on ESP32
```

Select your board under **Tools → Board → ESP32 Arduino** (usually ESP32 Dev Module). If ESP32
Arduino isn't listed, add the Espressif ESP32 board package (Chapters 2 and 7).

### Which ESP32 board package version should I use?

Use **2.0.17**.

- Not 2.0.15: its HardwareSerial is broken, so the LiDAR returns no data. Use 2.0.16 or newer.
- Not 3.x: it removed `ledcAttachPin` and `ledcSetup`, so the firmware won't compile.

### "use of deleted function MotorController()" or "ledcAttachPin was not declared"

The Arduino IDE 2.x Library Manager can silently replace the firmware's MotorController and PID
libraries with same-named ones. Copy the firmware's libraries back into your Arduino libraries
folder and rename them (for example `MotorController_kaia`).

!!! draft "Question for Ilia"
    If a library folder is renamed, do the sketch's `#include` lines need to change? A short
    step-by-step would help beginners.

### Upload fails with "Failed to connect to ESP32: No serial data received"

The upload stops at `Connecting......`:

```
esptool.py v4.5.3
Serial port COM3
Connecting......................................

A fatal error occurred: Failed to connect to ESP32: No serial data received.
```

Retry, and as soon as `Connecting...` appears, hold the ESP32's **BOOT** button for 3–5 seconds,
then release it. The same applies to sketch data (SPIFFS) uploads. Some boards don't need BOOT at
all.

### Upload fails on Ubuntu: "No module named 'serial'"

```
Traceback (most recent call last):
  File "/home/ilia/.arduino15/packages/esp32/tools/esptool_py/4.5.1/esptool.py", line 31, in <module>
    import esptool
  ...
  File "/home/ilia/.arduino15/packages/esp32/tools/esptool_py/4.5.1/esptool/loader.py", line 30, in <module>
    import serial
ModuleNotFoundError: No module named 'serial'
exit status 1
Error compiling for board ESP32 Dev Module.
```

Install pyserial (Chapter 7):

```
sudo apt install -y python3-pip
pip3 install pyserial
```

### Arduino IDE doesn't detect the ESP32 COM port

- Make sure the ESP32 is powered and its power LED is on.
- Try another USB cable. Some are **charge-only**, with no data wires.
- The ESP32's USB-to-serial chip can fail. Try the ESP32 on another PC, and another ESP32 on yours.

### SPIFFS upload fails: "No port specified" or "Could not open COM3"

```
SPIFFS Filesystem Uploader

Using partition: default
ERROR: No port specified, check IDE menus
```

Restart the Arduino IDE and retry.

```
Uploading SPIFFS filesystem
C:\Users\ilya\AppData\Local\Arduino15\packages\esp32\tools\esptool_py\4.5.1/esptool.exe --chip esp32 --port COM3 --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 2686976 C:\Users\ilya\AppData\Local\Temp\tmp-16336-VVuaXOVTskId-.spiffs.bin
esptool.py v4.5.1
Serial port COM3

A fatal error occurred: Could not open COM3, the port doesn't exist
ERROR: Upload failed, error code: 2
```

- **Close the Serial Monitor**, the most common cause; it holds the port.
- Make sure the ESP32 is connected and its USB serial port works.
- Try another PC, or another ESP32.

### SPIFFS upload fails: "SPIFFS_write error(-10010)"

```
SPIFFS_write error(-10010): unknown
error adding file!
```

A file name in the sketch's `data` folder is too long. Keep names to 30 characters or less.

### SPIFFS upload fails: "This chip is ESP32-S3 not ESP32"

```
A fatal error occurred: This chip is ESP32-S3 not ESP32. Wrong --chip argument?
SPIFFS Upload failed!
```

Select the correct board in the Arduino IDE.

### The SPIFFS upload command doesn't appear in Arduino IDE 2.x

Arduino IDE 2.x needs a separate SPIFFS upload plugin (Chapter 2): copy everything inside the
plugin's `.arduinoIDE` folder into `C:\Users\<your user name>\.arduinoIDE\plugins\` and restart the
IDE. If the command still doesn't show up, install Arduino IDE 1.8.19 with its SPIFFS plugin
alongside 2.x ([forum #87](https://github.com/makerspet/support/discussions/87)).

### SPIFFS upload fails on Ubuntu without a reason

The plugin builds the image, doesn't seem to try uploading, and fails:

```
[SPIFFS] upload : /tmp/arduino_build_928471/kaiaai-esp32.spiffs.bin
[SPIFFS] address: 2686976
[SPIFFS] port   : /dev/ttyUSB0
[SPIFFS] speed  : 921600
[SPIFFS] mode   : dio
[SPIFFS] freq   : 80m

SPIFFS Upload failed!
```

Upload the sketch data from a Windows PC instead. One builder saw this every time with Arduino IDE
1.8.19 on Ubuntu 24.04; Arduino IDE 2.x on Windows worked
([forum #70](https://github.com/makerspet/support/discussions/70)).

### The Serial Monitor prints garbage

- Set the Serial Monitor to 115200 baud.
- Press the ESP32's EN (reset) button. Garbage often appears right after a firmware upload.

### Which ESP32 boards are supported?

ESP32, ESP32-S3 and ESP32-E. Each has a matching config file in the firmware's
[data folder](https://github.com/kaiaai/firmware/tree/iron/kaiaai-esp32/data). The kit's board uses
the default [`config.yaml`](https://github.com/kaiaai/firmware/blob/iron/kaiaai-esp32/data/config.yaml).

!!! warning
    An ESP32-S3 config on a plain ESP32 (or the other way round) can make the board keep booting
    into WiFi setup (AP) mode: the configs use a different reset-button GPIO, so the button looks
    permanently pressed.

## B.5 WiFi and connecting to the ROS2 PC

### What the ESP32 activity LED tells you

| LED | Meaning |
|---|---|
| Solid on | AP mode: the ESP32 runs its own `KAIA.AI` WiFi hotspot for setup |
| Slow blinking, once per second | Connecting to your WiFi |
| Very slow blinking, once every 20 seconds | Connected to WiFi, connecting to the ROS2 PC |
| Fast blinking | Connected to the ROS2 PC |

### How to reset the WiFi configuration

To re-enter your WiFi name and password or your PC's IP address:

1. Power up the ESP32 (USB or battery).
2. Press the ESP32 reset (EN) button.
3. Within one second, press and hold BOOT. The LED blinks very fast.
4. Keep holding BOOT until the LED turns solid on.
5. Release BOOT. The ESP32 restarts in AP (WiFi configuration) mode.
6. Connect your phone or PC to the `KAIA.AI` WiFi, open `http://192.168.4.1`, enter your settings
   and click **Connect**. Connect saves the settings and restarts the ESP32; there's no Save button.

!!! tip
    While connected to `KAIA.AI`, you can check what the ESP32 stored at
    `http://192.168.4.1/network.yaml` (WiFi settings) and `http://192.168.4.1/config.yaml`
    (board configuration) ([forum #93](https://github.com/makerspet/support/discussions/93)).

### The ESP32 doesn't connect to WiFi

- Check the WiFi name and password you entered.
- Your WiFi must be **2.4 GHz**; the ESP32 doesn't support 5 GHz.
- Press the ESP32 reset (EN) button. This often helps if the WiFi is configured correctly.
- Make sure you uploaded the correct `config.yaml` for your board (see "Which ESP32 boards are
  supported?" above).
- Reset the WiFi configuration (above) and enter your settings again.

### The ESP32 connects to WiFi, but not to the ROS2 PC

The Serial Monitor keeps printing `Connecting to Micro-ROS agent ...` without `success`.

- Make sure the `kaiaai/kaiaai:iron` container is running and that inside it you launched
  `ros2 launch kaiaai_bringup physical.launch.py`.
- Make sure the robot and the PC are on the same local WiFi network.
- Cafe, restaurant and university WiFi often blocks devices from talking to each other ("client
  isolation"). Test with a phone hotspot
  ([forum #69](https://github.com/makerspet/support/discussions/69)).
- Make sure your PC's firewall accepts incoming local connections.
- Try disabling your antivirus. (Avast started blocking these ports in December 2025.)
- Check whether your PC's IP address has changed. If so, reset the WiFi configuration and enter the
  new address.

!!! draft "Question for Ilia"
    In [forum #93](https://github.com/makerspet/support/discussions/93) a Windows user who could ping
    the robot, with the firewall off, fixed it by binding the published ports to the PC's IP:
    `docker run ... -p <PC IPv4 address>:8888:8888/udp -p <PC IPv4 address>:4430:4430/tcp ...`.
    Recommend this as a last resort?

### Frequent CRC errors or "message(s) lost"

Frequent `RESULT_CRC_ERROR` and `N message(s) lost` lines in the ROS2 output (and "queue full"
stalls in RViz) almost always mean dropped WiFi packets, not a LiDAR fault.

- Keep the robot and the PC close to the WiFi router.
- Use a dedicated 2.4 GHz network, and avoid heavy WiFi use while the robot runs: video streaming,
  large downloads, cloud sync (OneDrive, for example).
- Check that the PC isn't short of CPU or memory, and that the battery isn't low.
- Keep the ESP32's PCB antenna a few centimetres clear of copper and other boards, above and below,
  with the antenna/USB end facing outward. Don't sandwich the ESP32 between the LiDAR and the main
  board. Prefer a module whose antenna sticks out past the board edge.
- If it happens on one robot only, try a known-good ESP32. Some modules transmit poorly
  ([forum #47](https://github.com/makerspet/support/discussions/47)).

### Micro-ROS errors in the Serial Monitor

```
rmw_uros_sync_session() error 1
OK
UTC time Thu Jan  1 00:00:06 1970
rclc_node_init_default(pet) error 1
addROSParams() error 1
...
rclc_executor_spin_some() error 1
rcl_publish(telem_msg) error 300
rclc_executor_spin_some() error 1
...
```

Press the ESP32 reset (EN) button.

## B.6 Docker and ROS2 on the PC

### `docker run` or `docker pull` fails: "error during connect"

```
docker: error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

The Docker engine isn't running. Start Docker Desktop and try again.

### `docker run` fails: "Ports are not available"

```
docker: Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:4430 -> 0.0.0.0:0: listen tcp 0.0.0.0:4430: bind: An attempt was made to access a socket in a way forbidden by its access permissions.
```

Reboot your Windows PC.

### `docker run` fails: container name "/makerspet" is already in use

```
docker: Error response from daemon: Conflict. The container name "/makerspet" is already in use by container "e86601354246...". You have to remove (or rename) that container to be able to reuse that name.
```

A `makerspet` container is still running from last time. Stop it and run `docker run` again:

```
docker container stop makerspet
```

To avoid this, exit all the container's shells when you finish instead of just closing the
PowerShell window.

### RViz or another GUI fails to start: "could not connect to display"

```
[rviz2-1] qt.qpa.xcb: could not connect to display host.docker.internal:0.0
[rviz2-1] qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
...
[ERROR] [rviz2-1]: process has died [pid 76, exit code -6, ...]
```

On Windows, start the X server before launching any GUI. On Ubuntu, check that you used the Ubuntu
`docker run` command (Chapter 7), not the Windows one.

### I can't get X11 working: view the GUIs over VNC instead

Use VNC (for example, instead of XQuartz on a Mac); TigerVNC and Xfce are in the image. Start the
container and the VNC server, then point a VNC viewer at `localhost:5901`:

```
docker run --name makerspet -it --rm -p 8888:8888/udp -p 4430:4430/tcp -p 5901:5901 -e DISPLAY=:1 kaiaai/kaiaai:iron
# then, inside the container:
vncserver :1 -geometry 1920x1080 -depth 24 -localhost no
```

### A ROS2 command doesn't exit even after Ctrl-C

From another Bash window in the container, list processes with `ps -al` and `kill` the stuck `ros2`
and `python3` processes by PID (here 334 and 272):

```
root@8ec422cb4258:/ros_ws# ps -al
F S   UID   PID  PPID  C PRI  NI ADDR SZ WCHAN  TTY          TIME CMD
4 S     0   272     1  0  80   0 - 107559 -     pts/0    00:00:00 ros2
4 S     0   334     1  0  80   0 - 210129 x64_sy pts/2   00:00:01 python3
4 R     0   713    66  0  80   0 -  1871 -      pts/1    00:00:00 ps
root@8ec422cb4258:/ros_ws# kill 334
root@8ec422cb4258:/ros_ws# kill 272
```

### The latest image misbehaves (for example, errors in `navigation.yaml`)

Try the previous image release, or the Jazzy image. For one builder, `kaiaai/kaiaai:iron-03-11-2025`
fixed a SLAM launch failure ([forum #82](https://github.com/makerspet/support/discussions/82)).
Images are tested with Docker, not Podman.

!!! draft "Question for Ilia"
    Is the `iron-03-11-2025` workaround from forum #82 still needed, or is the current
    `kaiaai/kaiaai:iron` fixed? If fixed, drop this entry.

### Windows WSL2 install fails

Follow Microsoft's [WSL installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install)
and [WSL troubleshooting page](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting).
As a last resort, run Ubuntu in a virtual machine (Appendix A); ROS2 will be laggy.

### How do I keep my changes when I restart the container?

A fresh container from the image loses changes made inside the old one. Commit the running container
to the image; to back it up off your PC, push it to your own Docker Hub repository:

```
docker container commit makerspet kaiaai/kaiaai:iron
# optional backup to your own Docker Hub repo:
docker tag kaiaai/kaiaai:iron <your-docker-hub-user>/kaiaai:iron
docker push <your-docker-hub-user>/kaiaai:iron
```

For the Jazzy image, use `kaiaai/kaiaai:jazzy`.

!!! warning
    Don't commit or publish an image that contains secrets, such as your WiFi credentials.

!!! draft "Question for Ilia"
    The web page's `docker tag` and `docker push` lines lost their placeholder in the HTML (it reads
    `docker tag kaiaai/kaiaai:iron /kaiaai:iron`). I've written `<your-docker-hub-user>`; please
    confirm.

### Running more than one robot from one PC

Simplest: one Docker container per robot, each with its own `--name` and host UDP port. Point each
robot's WiFi configuration at its port:

```
docker run --name makerspet1 ... -p 8888:8888/udp ... kaiaai/kaiaai:iron
docker run --name makerspet2 ... -p 8889:8888/udp ... kaiaai/kaiaai:iron
```

For true topic namespacing, edit the YAML files in `/ros_ws/src/makerspet_mini/config` (for example
[`telem.yaml`](https://github.com/makerspet/makerspet_mini/blob/iron/config/telem.yaml)), Turtlebot3
style. With the Jazzy image, each container gets its own network, so no `--ipc=host` is needed.

### Running the ROS2 side on a Raspberry Pi (ARM64)

The Docker image is x86-64 only, so on an ARM64 board such as a Raspberry Pi, install ROS2 natively:

1. Install Ubuntu 22.04 on the Pi.
2. Install ROS2 Iron with
   [`install_ros2_iron_ubuntu_22_04.sh`](https://github.com/kaiaai/install/blob/iron/ubuntu/install_ros2_iron_ubuntu_22_04.sh)
   (or the official ROS2 Iron Ubuntu instructions).
3. Install the Kaia.ai add-ons with
   [`install_kaiaai_iron.sh`](https://github.com/kaiaai/install/blob/iron/ubuntu/install_kaiaai_iron.sh).

For ROS2 Jazzy, use Ubuntu 24.04 with
[`install_ros2_jazzy_ubuntu_24_04.sh`](https://github.com/kaiaai/install/blob/jazzy/ubuntu/install_ros2_jazzy_ubuntu_24_04.sh)
and [`install_kaiaai_jazzy.sh`](https://github.com/kaiaai/install/blob/jazzy/ubuntu/install_kaiaai_jazzy.sh).

!!! note
    The kit's robot has no Raspberry Pi on board; the Pi only replaces the PC.

## B.7 LiDAR

Check in order: the LiDAR spins, the ESP32 captures its data, the data reaches ROS2.

### The LiDAR doesn't spin

The LiDAR should start spinning once the robot connects to the ROS2 PC. If it doesn't:

- Check the LiDAR wiring.
- Check that your model is on the [list of supported LiDAR models](https://github.com/kaiaai/kaiaai).
- Make sure the firmware and ROS2 are both configured for your model (see below). Both default to
  the LDROBOT LD14P.

### Check that the ESP32 captures LiDAR data

With the LiDAR spinning, watch the Serial Monitor telemetry. **LiDAR RPM must not be zero:**

```
Telem avg 46 max 52ms, LiDAR RPM 4.75, wheels RPM 0.00 0.00, battery 8.00V, RSSI -61dBm
Telem avg 46 max 52ms, LiDAR RPM 4.75, wheels RPM 0.00 0.00, battery 8.00V, RSSI -62dBm
```

`LiDAR RPM 0.00` means the ESP32 gets no LiDAR data. Check the wiring and the model configuration.

```
Telem avg 50 max 51ms, LiDAR RPM 0.00, wheels RPM 0.00 0.00, battery 0.99V, RSSI -59dBm
```

!!! note
    Look-alike models aren't necessarily compatible. A builder with an LDROBOT LD14 (not LD14P) saw
    `LiDAR RPM 0.00` and no scan in RViz; an LD14P fixed it
    ([forum #62](https://github.com/makerspet/support/discussions/62)).

### Check that LiDAR data reaches ROS2

Launch RViz:

```
ros2 launch kaiaai_bringup monitor_robot.launch.py
```

You should see live LiDAR points. If not, read the ROS2 terminal output:

- Check the printed LiDAR model (`LDS model ...`). If it isn't yours, the ROS2 side is misconfigured
  (see below).
- Look for CRC errors and "message(s) lost" lines. Unreliable WiFi causes them (B.5), and so can a
  wrong LiDAR model in the ROS2 configuration.

![The expected LiDAR model is printed; "message(s) lost" means dropped WiFi packets. From forum #25.](https://github.com/user-attachments/assets/c7fda637-d084-416d-a58a-f7c5d3da015b)

### Using a LiDAR other than the LD14P

Change the model in **two** places:

1. **The firmware.** In `config.yaml`'s `lidar:` section, comment out every `model:` line except
   yours, then upload the sketch data again. At boot, the Serial Monitor should print `LIDAR model`
   and your model.
2. **ROS2.** In the container, set `lidar_model` in `/ros_ws/src/makerspet_mini/config/telem.yaml`
   (for example `3IROBOTIX-DELTA-2G`). Commit the container to keep the change (B.6).

([forum #25](https://github.com/makerspet/support/discussions/25).) Wiring guides:

- [How to Connect YDLIDAR X3, X3PRO, X2, X2L, X4 and SCL to Maker's Pet ESP32 Boards](https://makerspet.com/blog/connect-ydlidar-x3-to-makerspet-esp32-boards/)
- [How to Connect Delta-2A, 2B and 2G LiDAR to Maker's Pet ESP32 Boards](https://makerspet.com/blog/connect-delta-2g-lidar-to-makerspet-esp32-boards/)
- [How-to: Connect Xiaomi $15 LDS02RR LiDAR to ESP32, Arduino](https://makerspet.com/blog/how-to-connect-xiaomi-lds02rr-lidar-to-esp32/)

<div class="pair" markdown="1">
![Delta-2G wired to the BDC-30P LiDAR port. From forum #25.](https://github.com/user-attachments/assets/efa3c748-385b-4ef0-a5e1-f2a4f095ffc0)
![LDS02RR connector pinout. From forum #45.](https://github.com/user-attachments/assets/ca33c694-9f5c-4e41-8da6-7238dcec8b82)
</div>

!!! tip
    The Delta-2G's TX outputs 5 V, not 3.3 V. You can put a resistor (100 Ω to 10 kΩ) in series with
    TX ([forum #25](https://github.com/makerspet/support/discussions/25)).

### Cheaper DIY adapter for the LDS02RR

If shipping the official LDS02RR adapter is too expensive, drive the LiDAR motor with a TB6612FNG
wired per the [LDS02RR-ADPT-V030 schematic](https://github.com/makerspet/store/blob/main/LDS02RR-ADPT-V030/schematic.pdf).
The connector location is in the product photos (and the pinout above, from
[forum #45](https://github.com/makerspet/support/discussions/45)), so you don't need to open the
housing. The adapter's manufacturing (CAM/CPL) files are no longer released.

### Which ESP32 pins for the LiDAR UART? (ESP32-S3, WROVER)

- **ESP32-S3:** hardware serial port 1 on GPIO17 (TX) and GPIO18 (RX).
- **ESP32-WROVER:** GPIO16 and GPIO17 are reserved for PSRAM. Move the LiDAR TX/RX to GPIO32/33.

If the LiDAR shuts off before reaching speed (a motor RPM error), raise `scan_rpm_err_thresh` to give
it time to spin up.

## B.8 Mapping and navigation

### Prepare your place first

- Block (with cardboard, for example) objects the LiDAR can't detect: black (non-reflective) and
  transparent objects, objects below the laser plane, very thin objects such as fine sparse mesh,
  mirrors and highly reflective objects, and objects lit by near-infrared-rich light (sunlight,
  incandescent bulbs).
- The robot can't drive over thick carpet or thresholds higher than about 5 mm (1/5″).
- Keep the scene still while mapping; don't open or close doors.
- Declutter, and leave plenty of space between obstacles.
- Block off ramps. Sloped flooring tilts the LiDAR's laser plane and messes up the map.

### "Goal Failed" errors

The robot can't find a safe path, usually because obstacles are too close together. It refuses a
path that passes too close to an obstacle, even without touching it.

- Make sure you have a clean map.
- Remove obstacles, and leave plenty of room between the rest.

![A clean map.](https://makerspet.com/wp-content/uploads/2026/04/clean_map.webp)

A slow PC can also fail navigation. Errors like
`Transform data too old when converting from odom to map` mean odometry processing took too long.
Close heavy programs, or use a faster PC.

Speed, inflation radius (how far the robot keeps from obstacles) and other settings are in
`/ros_ws/src/makerspet_mini/config/navigation.yaml` in the container
([on GitHub](https://github.com/makerspet/makerspet_mini/blob/iron/config/navigation.yaml)). For
tuning, search "ROS2 Nav2 tuning"; if you find better values, please share them on the forum.

!!! note
    If you've changed the robot's size (your own build), update it in the firmware `config.yaml`,
    the URDF and possibly `navigation.yaml`
    ([forum #60](https://github.com/makerspet/support/discussions/60)).

### The map is skewed or distorted

Map slowly, both driving straight and turning; fast motion makes SLAM skew the map badly. Check the
sensors first with `ros2 launch kaiaai_bringup monitor_robot.launch.py`, then map by driving with
teleop. Start with a simple room (one central obstacle).

If the map distorts specifically while the robot moves, also check encoder calibration (next).

### The map distorts, or the robot drives off the map (encoder calibration)

The real wheel speed probably doesn't match the commanded speed, usually because the encoder PPR
(pulses per revolution) in `config.yaml` is wrong.

1. Read the live values:

        ros2 param get /pet motor.encoder.ppr

    Also useful: `motor.left.encoder.now`, `motor.right.encoder.now`, `rpm.now`,
    `base.wheel.diameter` and `base.wheel.track`.

2. Count the encoder ticks over one full wheel revolution and divide by 4. The firmware multiplies
   the configured PPR by 4 for the quadrature edges, so enter the 1× value.
3. Set the correct PPR and a Max RPM the motor can actually reach, then upload the sketch data again.

!!! draft "Question for Ilia"
    The guide lists `motor.left/right.encoder.now` and `rpm.now`. I've expanded the first to
    `motor.left.encoder.now` / `motor.right.encoder.now`; please confirm the names, and whether
    `rpm.now` has a left/right prefix.

### The scan or map slides sideways when the robot drives straight

If the scan or map slides with the robot when driving straight, but turning looks right (and
odometry is calibrated), the LiDAR is mounted rotated relative to its URDF frame. Add the matching
yaw offset to the laser joint's `rpy`; for a LiDAR mounted 180 degrees round, add 3.14 rad.

### The robot moves too slowly during navigation

The Nav2 controller, not teleop, sets navigation speed. In `navigation.yaml`, `controller_server`
section, under `FollowPath`:

- `max_vel_x`: top forward speed in m/s (default 0.22), the main one. Raise it gradually, for
  example to 0.30, and set `max_speed_xy` to the same value.
- `max_vel_theta`: top turning speed in rad/s (default 1.0).
- `acc_lim_x` and `acc_lim_theta`: optionally raise these to reach target speed sooner.

[`config/teleop_keyboard.yaml`](https://github.com/makerspet/makerspet_mini/blob/iron/config/teleop_keyboard.yaml)
lists the drivetrain limit as `max_lin_vel: 0.4` m/s and `max_ang_vel: 7.72` rad/s (for the 200 RPM
motor, derated to 90%), so keep `max_vel_x` comfortably below 0.4. Higher speed leaves the planner
less time to react, so raise values in small steps and test.

Restart the navigation launch after editing. To keep the change, commit the container with the tag
of the image you run:

```
docker container commit makerspet kaiaai/kaiaai:iron
# or, if you run the Jazzy image:
docker container commit makerspet kaiaai/kaiaai:jazzy
```

### The robot makes a knocking sound

If you 3D-printed the parts, set **Seam Position** to **Random** in your slicer for the caster
wheel, or the seam can make it knock. Do the same for the wheels, or the robot may wobble slightly.

## B.9 Reference Serial Monitor output

### Healthy boot: connected to WiFi and the ROS2 PC

A working robot after a reset (boot ROM lines left out):

```
Kaia.ai firmware version 0.8.0-iron
ESP IDF version v4.4.7-dirty
SPIFFS mounted successfully
/network.yaml found; loaded OK
/config.yaml found; loaded OK
To enter web config push-and-release EN, then push-and-hold BOOT within 1 sec
Board model BDC-30P, version v1.1.0, manufacturer makerspet.com
LIDAR model LDROBOT LD14P
LIDAR RX buffer size 1024, baud rate 230400
Battery ADC attenuation 7.00, voltage 0.99V
Motor driver type IN1_IN2; motor encoder type AB_QUAD
Motor Max RPM 180.00; encoder PPR 1035.00 TPR 4140.00

Connecting to WiFi NETGEAR48 ... connected, IP 192.168.1.5
Connecting to Micro-ROS agent 192.168.1.113 ... success
Syncing time ... OK
UTC time Tue Feb 11 23:02:53 2025
micro-ROS client key 0xDD9181CC; ROS2 node /pet
Micro-ROS initialized
LiDAR info Model: LDROBOT LD14P
startLIDAR() result: OK

Telem avg 106 max 5667ms, LiDAR RPM 0.00, wheels RPM 0.00 0.00, battery 0.99V, RSSI -59dBm
Telem avg 50 max 51ms, LiDAR RPM 0.00, wheels RPM 0.00 0.00, battery 0.99V, RSSI -59dBm
```

This was captured on USB power with the battery off, hence about 1 V and zero LiDAR RPM. With the
battery on, expect your battery voltage and a non-zero LiDAR RPM (B.7).

Where it stops tells you where to look:

- Stops at `Setting up WiFi KAIA.AI; browse to http://192.168.4.1`: WiFi setup mode. Connect to
  `KAIA.AI` and configure it (B.5).
- Repeats `Connecting to WiFi ...`: see "The ESP32 doesn't connect to WiFi" (B.5).
- Repeats `Connecting to Micro-ROS agent ...`: see "The ESP32 connects to WiFi, but not to the ROS2
  PC" (B.5).

### Firmware uploaded, but no sketch data

A 30-pin ESP32 dev board prints:

```
Kaia.ai firmware version 0.8.0-iron
ESP IDF version v4.4.7-dirty
SPIFFS mounted successfully
Sketch data not found. Please upload sketch data.
```

Some boards (for example a 38-pin dev board with an ESP32-WROOM-32D module) print this instead:

```
E (43) SPIFFS: mount failed, -10025
```

Either way, upload the sketch data (Chapter 3).
