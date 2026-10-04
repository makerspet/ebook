# 1. Assemble the Robot

Video: [How to Create a Self-Driving LiDAR Robot with Arduino, ESP32, ROS2](https://youtu.be/6GtjAB19GP8)
{: .video-link }

You'll wire the motors to the BDC-30P driver board, assemble the chassis, fit the ESP32, battery
and LiDAR, and connect the ESP32 to your computer. No software is needed yet. Assembly takes about
an hour once you know the steps; allow more for your first build.

![The finished robot: ESP32, N20 motors and LiDAR.](yt:6GtjAB19GP8@0:05)

!!! note
    The video shows the February 2025 instructions. The "Since the video was recorded" boxes add
    later corrections from the bring-up and troubleshooting guide
    ([makerspet.com/blog/bld-120mm-pack/](https://makerspet.com/blog/bld-120mm-pack/)).

## What's in the kit and the tools you need

Lay everything out before you start:

- **Base plate** (round, white).
- **Board posts** (4) and **LiDAR posts** (4).
- **Caster wheel mounts** (2), the **roller** and its **metal shaft**.
- **Motor clamps** (2) and two **N20 gear motors with encoders**.
- **Wheels** (2) and **tires** (2).
- **Motor cables** (2): a plug on one end, loose wires on the other.
- **BDC-30P driver board** (open source).
- **Maker's Pet ESP32-E 30-pin dev kit module**, compatible with the original 30-pin ESP32 DOIT DevKit v1.
- **LDROBOT LD14P LiDAR** and its **breakout cable**.
- **LiDAR skirt** (the white ring that holds the LiDAR).
- **Battery case** for 6 AA batteries.
- **M3 screws** of two kinds: *countersunk* (flat head) screws go on the underside of the base;
  *hex button* (rounded head) screws go everywhere else.

Tools:

- A Phillips screwdriver for the countersunk screws and the screw terminals (an electric one is optional).
- A hex key or hex bit for the hex button screws.
- A wire stripper.
- A USB cable for the ESP32.

![The kit laid out.](yt:6GtjAB19GP8@0:16)

!!! tip "Printing the parts yourself"
    The 3D-printable parts are open source. The guide page has 3MF files for the base, LiDAR skirts,
    LiDAR posts, board posts, caster roller, caster mounts and the 2S battery holder backstop, plus
    the wheels and motor clamps, and the full Fusion 360 model.

    When slicing the **caster roller** and **wheels**, set *Seam Position* to **Random**. Otherwise
    the caster can knock rhythmically and the robot may wobble.

## Connect the motor wires to the board

Wire the screw terminals first, while the board is loose in your hand.

1. Unscrew all the board's wire terminals fully.

![Open up all the terminals fully.](frames/open_up_all_terminals.jpg)

2. Strip 8–10 mm of insulation off a motor wire.
3. Bend the bare strands back over the insulation. The thicker end grips better.
4. Insert the wire with the bare strands facing **up** and tighten the screw.

<div class="pair" markdown="1">
![Insert the wire with the metal on top.](yt:6GtjAB19GP8@0:31)
![Tighten the terminal screw.](frames/tighten_the_terminal_screw.jpg)
</div>

5. Connect the rest the same way, one motor cable per motor terminal block. Tug each wire gently to check it holds.

Both motor terminal blocks use the same order:

| Terminal | M2 | M1 | GND | ENCA | ENCB | +Venc |
|---|---|---|---|---|---|---|
| Wire color | red | white | blue | green | yellow | black |

!!! note
    These are the colors of the cables shipping now. Restocked cables may differ; if so, go by the
    pin order on the plug and the terminal labels on the board.

![Both motor cables wired in.](frames/bdc-30p-with-motor-wires-attached-on-both-sides.jpg)

!!! warning
    A loose screw terminal is the most common cause of a motor that "doesn't work", often because the
    stripped end is too short. If in doubt, strip longer than 8–10 mm (see
    [Troubleshooting](#troubleshooting-tips)).

## Build the chassis

### Posts

1. Attach the four **board posts**, the shorter posts, to the base plate with **countersunk M3 screws**. Orient each
   post's tab as shown: grab the post and its tab by hand and twist it carefully into place.

<div class="pair" markdown="1">
![Attach the board posts.](frames/attach_board_posts_process.jpg)
![All four board posts in place.](frames/attach_board_posts_result.jpg)
</div>

2. Attach the four longer **LiDAR posts** the same way, oriented as shown.

<div class="pair" markdown="1">
![Attach the LiDAR posts.](frames/attach_lidar_posts_process.jpg)
![Board and LiDAR posts in place, oriented as shown.](frames/attach_lidar_posts_result.jpg)
</div>

### Caster roller

1. Attach the two **caster wheel mounts** to the back of the base with **hex button M3 screws**, left slightly loose.

<div class="pair" markdown="1">
![Attach the caster mounts.](frames/attach_caster_mounts_process.jpg)
![Caster mounts in place.](frames/attach_caster_mounts_result.jpg)
</div>

2. Push the metal shaft through the roller.
3. Place the shaft ends into the two caster mounts.
4. Tighten the caster mount screws.
5. Press the roller against the table and roll the base back and forth until it spins freely.

<div class="pair" markdown="1">
![Push the shaft through the roller.](frames/insert_roller_shaft_process.jpg)
![Place the shaft ends into the caster mounts.](frames/attach_roller_process.jpg)
</div>

<div class="pair" markdown="1">
![Roller in place, bottom view.](frames/base_with_pcb_lidar_posts_and_roller_view_from_bottom.jpg)
![Tighten the caster mount screws.](frames/tighten_caster_screws_process.jpg)
</div>

<div class="pair" markdown="1">
![Roll the base to loosen the roller.](frames/loosen_the_roller_process.jpg)
![Posts and roller in place, top view.](frames/base_with_pcb_lidar_posts_and_roller_view_from_top.jpg)
</div>

### Motors

1. Insert each motor into its clamp, front face flush with the clamp.
2. Attach each motor to the base with **three countersunk M3 screws**, shafts pointing outward.
3. Don't overtighten; it can bend the plastic base.

<div class="pair" markdown="1">
![Insert the motor into the motor clamp.](yt:6GtjAB19GP8@1:42)
![Screw the motor to the base; don't overtighten.](yt:6GtjAB19GP8@2:05)
</div>

![Both motors mounted, shafts pointing out.](yt:6GtjAB19GP8@2:08.5)

<div class="keep" markdown="1">
!!! update "Since the video was recorded"
    Check that no board post tab touches a motor. A post pressing on a motor can block it, and a
    blocked motor can burn out when powered. If one does, twist the post to turn its tab away.

![Make sure the board post tab doesn't touch the motor.](https://makerspet.com/wp-content/uploads/2026/04/pcb_post_touches_motor.webp)
</div>

!!! update "Since the video was recorded"
    Bent plastic, including the base, can rub against the motor gears or encoder disk, stall the
    motor and burn it out. Tighten the motor screws just until snug.

### Wheels

1. Make sure each wheel is free of debris.
2. Press a tire into each wheel's groove all the way around.

<div class="pair" markdown="1">
![Put the tire on the wheel.](frames/attach_tire_process.jpg)
![Press the tire into the groove with your fingers.](frames/press_tire_in_using_your_fingers.jpg)
</div>

3. Find the flat on the motor shaft and the matching flat in the wheel's hub.

<div class="pair" markdown="1">
![The flat on the motor shaft.](frames/motor_shaft_flat_being_pointed_out.jpg)
![The flat in the wheel hub.](frames/wheel_shaft_pocket_flat_being_pointed_out.jpg)
</div>

4. Line up the flats and press the wheel fully onto the shaft with both hands.
5. Spin each wheel by hand to check it doesn't rub.

![Press the wheel fully onto the shaft with both hands. Check wheel rotation.](frames/press_wheel_onto_shaft_fully_with_both_hands.jpg)

!!! update "Since the video was recorded"
    Grit or plastic shavings in the gearbox can jam the gears and burn out the motor. That's why you
    clean the wheels and hubs first.

## Mount the board

1. Line up each motor cable's plug with the connector on the back of the motor and press it in gently. If it won't go in, check the alignment rather than forcing it.

<div class="pair" markdown="1">
![Align the plug with the motor's receptacle.](frames/align_plug_with_the_motors_receptacle.jpg)
![Press the plug in gently.](frames/press_plug_into_motor_receptable_gently.jpg)
</div>

2. Route the cables under the board and gently bend the wires down at the motor plugs.

![Route cables under the board. Bend the wires down at the motor plugs gently.](yt:6GtjAB19GP8@2:50)

3. Attach the board to the posts with **four hex button M3 screws**.

![Attach the board to the posts.](frames/attach_board_to_posts_using_screws.jpg)

!!! tip
    Before plugging in each cable, check the motor's connector: its plastic housing can slide up
    off its pins. See [Troubleshooting](#troubleshooting-tips).

## Connect the battery

1. Connect the battery case wires to the `+BAT`, `GND`, `ExtVmot` screw terminal: red to `+BAT`, black to `GND`.
2. Check the polarity **before** switching on. Reversed polarity will burn the board.
3. This time, **don't** fold back the stripped conductors; insert them straight.

![Battery wires in the screw terminal: red to +BAT, black to GND.](frames/positive_and_negative_battery_wires_attached_to_board_screw_terminals.jpg)


## Insert the ESP32 module

Plug the **Maker's Pet ESP32-E 30-pin dev kit module** into the board's socket with its USB
connector toward the **battery screw terminals**. Check before pressing it fully in: backwards, it
gets the wrong power pins.

![Insert the ESP32 module. Check the orientation.](frames/check_the_module_orientation.jpg)

!!! note
    I test and support the kit with the Maker's Pet ESP32-E, which is compatible with the original
    30-pin ESP32 DOIT DevKit v1. Clones from other makers might work, but aren't supported.

## Prepare the LiDAR

1. Attach the **LiDAR skirt** to the LiDAR with **three M3 hex button screws**, leaving no gaps.

<div class="pair" markdown="1">
![Attach the LiDAR skirt.](frames/attach_lidar_skirt.jpg)
![No gaps between skirt and LiDAR.](yt:6GtjAB19GP8@3:40.5)
</div>

## Batteries

1. Make sure the board's power switch is **OFF**.
2. Put 6 × AA batteries into the case and place it on the base as shown.

<div class="pair" markdown="1">
![Make sure the power switch is OFF.](frames/make_sure_power_switch_is_off.jpg)
![Place the battery case.](frames/place_the_battery.jpg)
</div>

!!! update "Since the video was recorded: 18650 rechargeable battery holder mod"
    The BDC-30P is designed for **non-rechargeable alkaline** batteries (6 × AA) and has no
    protection for rechargeable cells, which can be dangerous when mishandled. **Using rechargeable
    batteries is at your own risk.**

    If you still use a 2-cell 18650 holder (it fits the 120 mm base):

    - Use **protected** cells only (short-circuit, overcurrent, overcharge and overdischarge protection), connected **in series**.
    - Charge the cells out of the holder in your own charger.
    - Choose cells rated for around 3 A continuous and 5 A peak.
    - Mount the rear posts in the **outer spare holes** of the base.
    - Mount the battery holder backstop behind the battery in the two spare holes, with two M3 countersunk screws.
    - Use the **wider LiDAR skirt** that matches the new rear post positions.

![The 18650 battery holder mod.](https://makerspet.com/wp-content/uploads/2026/04/Mini_with_BDC_30P_18650_battery_holder.webp)

## Connect the LiDAR

1. Connect the LiDAR breakout cable wires to the board's `LIDAR` header:

    | Header pin | GND | TX | PWM | +5V |
    |---|---|---|---|---|
    | Wire color | black | yellow | red | green |

    Restocked cables may use other colors; go by the pin labels.

![Connect the LiDAR wires to the board.](frames/connect_lidar_wires.jpg)

2. Line the plug up with the LiDAR's connector and push it in gently until it clicks.
3. Fold the wires neatly and place the LiDAR on the robot.

<div class="pair" markdown="1">
![Align the plug and push it in gently until it clicks.](frames/align_plug_with_lidar_connector_and_push_plug_in_gently_until_click.jpg)
![Fold the wires and place the LiDAR.](frames/fold_wires_and_place_lidar.jpg)
</div>

Don't fix the LiDAR in place until after the firmware upload.


## Connect to your computer

Place the LiDAR carefully aside on the table, still connected to the board, to reach the ESP32-E's
USB connector. Connect the ESP32 to your computer with a USB cable. The robot is ready for the
firmware upload.

![Ready to upload the firmware!](yt:6GtjAB19GP8@4:32)

!!! tip
    If your computer doesn't see the ESP32, try another USB cable. Some carry power only.

## Troubleshooting tips

**A screw terminal connection fails.** Usually the stripped end is too short. Strip it even longer
than in the video.

![Strip wires even longer than shown.](frames/even_longer_than_shown.jpg)

**A screw won't hold in plastic.** Overtightening stripped the thread. Push a small wood splinter
into the hole and drive the screw back in.

![Insert a wood splinter to fix the thread.](frames/insert_a_splinter_to_fix_thread.jpg)

**The motor connector housing has slid up.** The plastic housing can slide up, off the connector
pins. Press it back down fully before plugging in the cable.

![The connector housing slid up fully; press it back down.](frames/slide_connector_housing_up_fully.jpg)

**One motor works, the other doesn't.** Swap the two motors' connections. If the problem moves
sides, the motor (or its cable) is at fault; if it stays, check that side's screw terminals.

![Swap the two motors' connections.](frames/swap_two_motors_connections.jpg)

**Check the green encoder lights.** With the battery on, each motor's encoder board should show a
green light. If one is off, that encoder has no power: check the battery, the switch, and the
motor-to-cable and cable-to-board connections.

![Check the motor encoder lights.](frames/check_motor_encoder_lights.jpg)

!!! update "Since the video was recorded: more motor checks from the guide"
    - No **board post tab touches a motor** (see *Motors*).
    - The **power switch is ON**, the battery is connected and not low. The ESP32's power LED should light.
    - The motor wires are in the **correct screw terminals**, none broken or loose.
    - **No debris in the gearbox**; it can seize the gears and burn out the motor.
    - **Motor screws not overtightened**; bent plastic can catch the gears or encoder disk.
    - Gently spin the magnet to turn the motor's core shaft. If it turns freely, the gearbox may be seizing.
    - Encoder sensors can get bent and touch the encoder wheel. Carefully bend them back and check the encoder magnet turns freely.
    - No cable rubs on a motor's encoder magnet.

    Checks that need the firmware and ROS2 running, such as a motor that spins only at full speed
    or in one direction, are in the bring-up chapter.

!!! update "Since the video was recorded: battery connected but no power"
    - Check the board's ON/OFF switch.
    - Check the battery wires are in the right terminals with good contact; measure the voltage at the board's power terminal.
    - Check the **polarity**. Reversed polarity will burn the board.
    - Check the batteries make good contact in the holder (wiggle tight ones) and measure each one.

Next, set up the software and upload the firmware.

![The finished robot. Happy building!](frames/the_finished_robot.jpg)
