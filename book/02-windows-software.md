# 2. Set Up the Software on a Windows PC

Video: [Step by Step Arduino Self-Driving Robot software setup](https://youtu.be/IOQBNl0O_tI)
{: .video-link }

This chapter has two halves. First, install the Arduino IDE with the ESP32 toolchain and the robot
firmware, and check that the firmware compiles. Second, install the PC side that controls the
robot: ROS2 runs on Linux, so you add WSL2, Docker Desktop, an X server (to see Linux GUI programs)
and PowerShell, then download the robot software image.

You need a Windows 10 (or later) PC with at least 8 GB of RAM and an internet connection, but not
the robot. Expect large downloads and a couple of reboots.

!!! note
    On Ubuntu Linux, skip to Chapter 7 instead. For simulation only (Chapter 6), skip the Arduino
    part: install WSL2, Docker Desktop, the X server and PowerShell, and download the Docker image.

!!! tip "Which Arduino IDE?"
    Both Arduino IDE 2.x and 1.8.19 work. I recommend **1.8.19**: it's tried and true, and frozen,
    so it won't change under you, while 2.x has given me some headaches. This chapter covers 2.x
    first, then [1.8.19](#if-you-prefer-arduino-ide-1-8-19).

## Install Arduino IDE 2

1. On arduino.cc, open **Software** and under **Arduino IDE 2.x** download the first **Windows**
   option (Win 10 and newer, 64 bits). The video used Arduino IDE 2.3.4.
   ![Arduino IDE 2 download options.](yt:IOQBNl0O_tI@0:28#crop=0,0,0.94,0.86)
2. Run the installer, accept the defaults, and launch the IDE. If Windows Firewall asks, click
   **Allow**.

## Add the Espressif ESP32 toolchain

The robot's brain is an ESP32, so the IDE needs Espressif's ESP32 compiler and SDK.

1. Go to **File → Preferences**. In **Additional boards manager URLs**, paste this URL and click
   **OK**:

    ```
    https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
    ```

    ![File → Preferences: paste the Espressif URL and click OK.](frames/open_file_preferences_in_arduino_2_paste_espressive_toolchain_url_and_click_ok.jpg#crop=0.19,0.26,0.68,0.72)
2. Go to **Tools → Board → Boards Manager**.
3. Search for `Espressif`. For **esp32 by Espressif Systems**, select version **2.0.17**, not the
   newest, and click **INSTALL**. Then close the IDE.
   ![Select version 2.0.17.](yt:IOQBNl0O_tI@1:16#crop=0.19,0.25,0.3,0.44)

!!! update "Since the video was recorded"
    Stay on ESP32 board package **2.0.17**:

    - Not **2.0.15**: its HardwareSerial is broken, so the firmware compiles but the LiDAR returns
      no data. 2.0.16 or newer works; 2.0.17 is recommended.
    - Not **3.x**: it removed `ledcAttachPin`/`ledcSetup`, which the firmware uses.

## Download the robot firmware project

1. Browse to [github.com/kaiaai/firmware](https://github.com/kaiaai/firmware) and click
   **Releases**.
   ![The kaiaai/firmware repository; Releases is on the right.](yt:IOQBNl0O_tI@1:34)
2. In the latest release, expand **Assets** and download **Source code (zip)**.
   ![Download Source code (zip).](yt:IOQBNl0O_tI@1:38)
3. Open the ZIP (`firmware-0.8.6.zip` at the time of writing) and step into its `firmware-*` folder. It
   holds `.arduinoIDE`, `kaiaai-esp32`, `libraries`, `tools` and a few files.
   ![Inside the firmware-* folder.](frames/inside_the_firmware_folder.jpg#crop=0.34,0.32,0.66,0.66)
4. Copy **everything** in that folder into your Arduino sketch folder, usually
   `Documents\Arduino`. This installs the firmware project and the tested versions of the
   libraries it needs.
   ![Copy everything into your sketch folder.](frames/copy_everything_into_your_sketch_folder.jpg#crop=0,0.31,1,0.68)

!!! tip
    Your sketch folder is shown as **Sketchbook location** in **File → Preferences**. With
    OneDrive, it may be under OneDrive, as in the video.

## Install the Arduino IDE plugin

The `arduino-spiffs-upload` plugin uploads the robot's configuration files to the ESP32 later.

1. In the ZIP, go into `.arduinoIDE`, then `plugins`.
2. Copy everything in it into your Arduino IDE plugins folder, creating it if needed:

    ```
    C:\Users\YourUserName\.arduinoIDE\plugins\
    ```

    Replace `YourUserName` with your Windows user name.

    ![Copy arduino-spiffs-upload-1.1.5.vsix into your .arduinoIDE\plugins folder.](frames/copy_arduino-spiffs-upload_into_your_plugins_folder.jpg#crop=0,0.32,1,0.68)

## Compile the firmware

1. Launch the Arduino IDE. If it offers library or board updates, click **LATER**. Newer versions
   can break compilation.
   ![Click LATER on update offers.](yt:IOQBNl0O_tI@2:20)
2. Go to **File → Open** and open the `kaiaai-esp32` sketch from your sketch folder.
3. Click the board selector, choose **Select other board and port**, search for `doit`, select
   **DOIT ESP32 DEVKIT V1** and click **OK**. No port is needed to compile.
   ![Select DOIT ESP32 DEVKIT V1.](frames/select_doit_esp32_devkit_v1.jpg#crop=0.18,0.18,0.68,0.70)
4. Click **Verify** (check mark). Compiling can take a few minutes and should end with no errors
   and a memory summary.
   ![The firmware compiled.](frames/the_firmware_compiled.jpg#crop=0.18,0.18,0.68,0.81)

!!! update "Since the video was recorded"
    Arduino IDE 2.x's Library Manager can silently replace the bundled `MotorController` and `PID`
    libraries with same-name libraries by other authors, causing errors like
    `use of deleted function MotorController()` or `ledcAttachPin was not declared`. Prevent this by
    renaming the kaiaai libraries in `Documents\Arduino\libraries` (for example to
    `MotorController_kaia`).

!!! tip "Compile error: `#error This code runs on ESP32`"
    No ESP32 board is selected. Select it as in step 3. If no ESP32 boards are listed, add the
    Espressif toolchain first.

## If you prefer Arduino IDE 1.8.19

Use this instead of IDE 2; otherwise skip to [Install Windows WSL2](#install-windows-wsl2).

1. On arduino.cc **Software**, under **Legacy IDE (1.8.X)**, download **Arduino IDE 1.8.19** for
   Windows (Win 7 and newer). Install and launch it.
   ![Arduino IDE 1.8.19 in the Legacy IDE section.](yt:IOQBNl0O_tI@2:56)
2. In **File → Preferences**, paste the same Espressif URL into **Additional Boards Manager URLs**.
   In **Tools → Board → Boards Manager**, search for `esp32`, select version **2.0.17** of
   **esp32 by Espressif Systems** and click **Install**.

<div class="pair" markdown="1">
![File → Preferences in IDE 1.8.19.](yt:IOQBNl0O_tI@3:26)
![Boards Manager: esp32 2.0.17.](yt:IOQBNl0O_tI@3:38)
</div>

3. Copy the firmware project into `Documents\Arduino` as in
   [Download the robot firmware project](#download-the-robot-firmware-project). With IDE 1.8.19,
   the copied `tools` folder adds **Tools → ESP32 Sketch Data Upload**; skip the plugin step.
4. Go to **File → Open** and open `Documents\Arduino\kaiaai-esp32`.
5. Go to **Tools → Board → ESP32 Arduino** and select **ESP32 Dev Module**.
   ![Select ESP32 Dev Module.](yt:IOQBNl0O_tI@4:06)
6. Click **Verify**. It can take a few minutes and should finish with no errors.
   ![Compiling in Arduino IDE 1.8.19.](yt:IOQBNl0O_tI@4:16)

## Install Windows WSL2

ROS2, the software that controls the robot, runs on Linux. WSL2 (Windows Subsystem for Linux) runs
Linux on your Windows PC.

1. Click **Start**, type `cmd`, and on **Command Prompt** choose **Run as administrator**.
   ![Run Command Prompt as administrator.](yt:IOQBNl0O_tI@4:22)
2. Run this command and wait until it reports success:

    ```
    wsl --install --no-distribution
    ```

    ![WSL2 installed; reboot to finish.](yt:IOQBNl0O_tI@4:37#crop=0.12,0.2,0.58,0.42)
3. Reboot your PC.

!!! update "Since the video was recorded"
    If WSL2 fails to install, follow Microsoft's WSL installation and troubleshooting instructions
    on learn.microsoft.com. As a last resort, run Ubuntu in a virtual machine (Appendix A), though
    in my experience it makes ROS2 laggy.

## Install Docker Desktop

Docker installs and runs a large collection of robotics software in one go.

1. Go to docs.docker.com/desktop/install/windows-install/ and download
   **Docker Desktop for Windows - x86_64** (for a typical Intel or AMD PC).
   ![Download the x86_64 installer.](yt:IOQBNl0O_tI@4:54)
2. Run `Docker Desktop Installer.exe`, keep **Add shortcut to desktop** checked and click **OK**.
3. At **Installation succeeded**, click **Close and restart**.
   ![Click Close and restart.](yt:IOQBNl0O_tI@5:22)

!!! note
    Docker Desktop is free for personal use; commercial use in larger enterprises requires a paid
    subscription.

## Install the X server

The X server shows the Linux robot software's GUI, such as the map view, on your Windows desktop.
The video uses VcXsrv.

1. Browse to [sourceforge.net/projects/vcxsrv/](https://sourceforge.net/projects/vcxsrv/) and click
   **Download**.
   ![Download VcXsrv from SourceForge.](yt:IOQBNl0O_tI@5:34)
2. Run the `vcxsrv` installer with the default components and folder.

!!! note
    SourceForge says VcXsrv has moved to
    [github.com/marchaesen/vcxsrv](https://github.com/marchaesen/vcxsrv). The SourceForge download
    worked in the video.

## Launch Docker Desktop and the X server

1. Launch **Docker Desktop** from its desktop icon. No account is needed: click **Skip** on the
   sign-in screen and the survey. Once Docker Engine has started, close the window; the engine
   keeps running.

<div class="pair" markdown="1">
![Click Skip.](yt:IOQBNl0O_tI@6:00)
![Starting the Docker Engine.](yt:IOQBNl0O_tI@6:04)
</div>

2. Launch **XLaunch** from your desktop. On **Display settings**, set **Display number** to `0`
   (zero), keep **Multiple windows** and click **Next**. Accept the remaining defaults and click
   **Finish**.
   ![Set Display number to 0.](yt:IOQBNl0O_tI@6:10)

!!! tip
    Launch the X server after every PC restart, before starting any robot GUI. If RViz or another
    ROS2 GUI reports `could not connect to display`, the X server isn't running.

## Install PowerShell

You will type the robot's Docker commands in PowerShell.

1. Browse to [github.com/PowerShell/PowerShell](https://github.com/PowerShell/PowerShell) and click
   **Releases**.
   ![Open the PowerShell releases.](yt:IOQBNl0O_tI@6:22)
2. In the latest release's **Assets**, download `PowerShell-<version>-win-x64.exe` (in the video,
   `PowerShell-7.5.0-win-x64.exe`).
   ![Download the win-x64.exe asset.](yt:IOQBNl0O_tI@6:26#crop=0.25,0.55,0.55,0.4)
3. Run the installer.
4. Click **Start**, type `powershell` and launch **PowerShell 7 (x64)**. Pin it to the taskbar.
   ![PowerShell 7 (x64), not the older Windows PowerShell.](yt:IOQBNl0O_tI@6:40)

## Download the robot software image

1. Make sure Docker Desktop is running.
2. In PowerShell, type:

    ```
    docker pull kaiaai/kaiaai:iron
    ```

    ![docker pull in PowerShell.](yt:IOQBNl0O_tI@6:48)
3. The image is large. When done, PowerShell shows
   `Status: Downloaded newer image for kaiaai/kaiaai:iron`.
   ![The image has downloaded.](yt:IOQBNl0O_tI@6:51#crop=0.04,0.08,0.73,0.67)

!!! warning "`docker pull` fails with `error during connect`"
    An error like this:

    ```
    error during connect: Post "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/...": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
    ```

    means the Docker engine isn't running. Launch Docker Desktop, wait for the engine, and retry.

!!! update "Since the video was recorded"
    A ROS2 Jazzy image, `kaiaai/kaiaai:jazzy`, is also available. This book uses the Iron image,
    `kaiaai/kaiaai:iron`.

The software is installed. Next, you will upload the firmware and bring up the robot.
