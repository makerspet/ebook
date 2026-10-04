# Appendix A. Run Ubuntu in a Virtual Machine on Windows

Video: [How to set up Ubuntu 22.04 on a Windows PC - using a virtual machine](https://youtu.be/q9uG86FcqVA)
{: .video-link }

!!! note "Use this only if WSL2 won't install"
    I don't recommend this approach: in my experience, a virtual machine makes ROS2 laggy. Use WSL2
    if you can.

Here you will create a virtual machine (VM) with VMware Workstation Player, free for personal use,
and install Ubuntu 22.04 in it. Then continue with Chapter 7, running every command inside the VM.
You can keep Arduino IDE on Windows (Chapter 2) instead of installing it in the VM.

You need about 50 GB of free disk space and enough RAM to give the VM at least 4 GB; 16 GB in the
PC is comfortable.

## Install VMware Workstation Player

1. Download the VMware Workstation installer for Windows. It's now free for personal, educational
   and commercial use, with no license key. The video uses VMware Player 17.6.3.

    !!! tip "Where to download"
        I've had a good experience downloading it from TechSpot (search for "VMware Workstation
        TechSpot"). You can also download it directly from Broadcom, but that needs a Broadcom
        account and, in my experience, is a hassle.

2. Run the installer, accept the license agreement and click **Next**.
3. On **Custom Setup**, keep the default folder
   (`C:\Program Files (x86)\VMware\VMware Player\`) and the **Add VMware Workstation console tools
   into system PATH** checkbox. Click **Next**.

    ![Custom Setup page.](yt:q9uG86FcqVA@0:36#crop=0.33,0.26,0.34,0.47)

4. On **User Experience Settings**, choose your update and Customer Experience options and click **Next**.

5. Keep the shortcuts, click **Next**, then **Install**.

## Download Ubuntu 22.04

1. While VMware installs, search for "Ubuntu 22.04 download" to reach `releases.ubuntu.com/jammy/`
   (22.04.5 LTS at the time of recording).
2. Under **Desktop image**, click **64-bit PC (AMD64) desktop image**. The `.iso` is several gigabytes.

![Download the 64-bit desktop image.](yt:q9uG86FcqVA@0:59)

!!! tip
    Download 22.04, not the newest release. The robot's ROS2 software is set up for 22.04.

## Create the virtual machine

1. Launch VMware Workstation Player and click **Create a New Virtual Machine**.

2. Select **Installer disc image file (iso)**, click **Browse...** and pick the Ubuntu `.iso`.
   VMware detects "Ubuntu 64-bit 22.04.5" and will use Easy Install. Click **Next**.

    ![Select the downloaded Ubuntu image.](yt:q9uG86FcqVA@1:16#crop=0.175,0.24,0.27,0.5)

3. Enter your full name, Ubuntu user name and password. Click **Next**.

    ![Easy Install Information.](yt:q9uG86FcqVA@1:25#crop=0.175,0.24,0.27,0.5)

4. Name the VM, for example `Ubuntu 22.04`, and set **Location** outside OneDrive, for example
   `C:\Users\<you>\VM\Ubuntu 22.04`. Click **Next**.

    ![Name the VM and store it outside OneDrive.](yt:q9uG86FcqVA@1:40#crop=0.175,0.24,0.27,0.5)

    !!! warning "Keep VM files off OneDrive"
        The default location is `...\OneDrive\Documents\Virtual Machines\`. OneDrive would keep
        backing up the huge, constantly changing VM files, slowing your PC and network.

5. On **Specify Disk Capacity**, I set **Maximum disk size** to `50` GB instead of the recommended
   20 GB and choose **Store virtual disk as a single file**. The file grows as needed. Click **Next**.

    ![50 GB disk, single file.](yt:q9uG86FcqVA@1:46#crop=0.175,0.24,0.27,0.5)

6. On **Ready to Create Virtual Machine**, click **Customize Hardware...**.
7. Set **Memory** and **Processors**. My PC has 16 GB and 8 cores, so I give the VM 8 GB (8192 MB)
   and 4 cores. Use at least 4 GB. Click **Close**.

    ![8 GB memory and 4 processor cores.](yt:q9uG86FcqVA@1:58#crop=0.075,0.08,0.47,0.83)

8. Leave **Power on this virtual machine after creation** checked and click **Finish**.

    ![Summary: 50 GB disk, 8192 MB memory, 4 CPU cores.](yt:q9uG86FcqVA@2:01#crop=0.175,0.24,0.27,0.5)

## Install Ubuntu in the VM

The VM boots into the Ubuntu installer.

1. Choose your keyboard layout and click **Continue**.
2. Follow the installer's prompts. Its defaults work; the disk it erases is the VM's virtual disk,
   not your Windows drive.
3. When **Installation Complete** appears, click **Restart Now**, then log in.

!!! warning
    If Ubuntu offers to upgrade to 24.04, decline. The robot software in this book needs 22.04.

## Remove unneeded hardware and set up networking

1. Shut down the VM: system menu (top right) > **Power Off / Log Out** > **Power Off...**.
2. If VMware shows a **Removable Devices** hint, click **OK**. Each USB device connects either to
   Windows or to the VM, not both.

3. In VMware Workstation Player, right-click your `Ubuntu 22.04` VM and choose **Settings...**.

    ![Open the VM settings.](yt:q9uG86FcqVA@4:30#crop=0.045,0.085,0.46,0.7)

4. Select and **Remove** the leftovers from Easy Install: both **CD/DVD (SATA)** drives (the Ubuntu
   `.iso` and `autoinst.iso`) and the **Floppy** (`autoinst.flp`).

    ![Remove the CD/DVD drives and the floppy.](yt:q9uG86FcqVA@4:42#crop=0.04,0.01,0.48,0.85)

5. To make the VM reachable from your local network, select **Network Adapter** and change
   **Network connection** from **NAT** to **Bridged: Connected directly to the physical network**.
   Keep **Replicate physical network connection state** checked.

    ![Set the network connection to Bridged.](yt:q9uG86FcqVA@4:52#crop=0.04,0.01,0.48,0.85)

    !!! tip "Why bridged?"
        With NAT the VM hides behind your PC's IP address. Bridged gives it its own address on your
        network, like a separate computer.

6. Click **Configure Adapters** and check only the physical adapter you use. My PC is on Wi-Fi, so I
   keep only **Realtek 8822CE Wireless LAN 802.11ac PCI-E NIC**. Your names will differ. Click **OK**.

    ![Bridge to the Wi-Fi adapter only.](yt:q9uG86FcqVA@5:02#crop=0.045,0.045,0.2,0.29)

7. Click **OK** and launch the VM.

## Install the robot software and connect USB devices

Continue with Chapter 7 to install Arduino, Docker and ROS2, running every command inside the VM.

When you plug in a USB device, such as the robot's ESP32 board, VMware asks whether to connect it to
Windows (the host) or to the VM.

![Connect the ESP32's CP2102 USB-to-UART bridge to the host or the VM.](yt:q9uG86FcqVA@5:26#crop=0.355,0.365,0.29,0.28)

- **Connect to the host** if Arduino IDE runs on Windows.
- **Connect to a virtual machine** (`Ubuntu 22.04`) if Arduino IDE runs in the VM.

Don't check **Remember my choice and do not ask again** until you're sure.
