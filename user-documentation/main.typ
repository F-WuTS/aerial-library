#let title = "Getting started with the aerial-library"
#set document(
    title: title,
    author: "Konstantin Lindorfer",
)

#set page(
    paper: "a4",
    header: align(center)[
        #set text(fill: luma(150))

    ],
    footer: context [
        #set text(fill: luma(150))

        #datetime.today().display()
        #h(1fr)
        #smallcaps(title)
        #h(1fr)
        Page #counter(page).display("1 of 1", both: true)
    ],
)

#set par(justify: true)
#set text(lang: "en", hyphenate: false)
#set heading(numbering: "1)")
#set enum(numbering: "1)")
#show link: underline

#let code_dist = 0.5em
#show raw: it => box(
    fill: luma(240),
    inset: (left: code_dist, right: code_dist),
    outset: (top: code_dist, bottom: code_dist),
    radius: 0.25em,
    text(0.95em, it)
)

#align(center, std.title())
#v(3em)


This document guides students through the setup process for the aerial-library.
Supervision by a teacher or mentor is highly recommended,
as some steps may require expertise regarding your computer's operating system.


= What you need
- bitcraze STEM drone bundle
  - Crazyflie 2.x
  - Flow deck v2
  - Multi-ranger deck
  - Crazyradio 2.0
- Laptop or other personal computer
  - USB port
  - Python


= Assemble the drone
Complete the drone assembly according to the official guide: \
https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyflie-2-x/#assembling.

Also attach the Flow deck to the bottom of the drone, and the Multi-ranger deck to the top of the drone in place of the battery holder.


= Set up a development environment
Since you should not install Python libraries directly to your computer, set up a *virtual~environment* first.

+ Create a folder somewhere on your computer.

  Example (Windows): ```sh C:\Users\YOU\Documents\aerial-competition``` \
  Example (Linux): ```sh /home/YOU/Documents/aerial-competition```

+ Open a terminal and navigate to your project folder.

+ Create the virtual environment for installing Python libraries.
  In your *project folder*, invoke the python module "venv" and call the target folder for the virtual environment "venv".

  Windows: ```sh py -m venv venv``` \
  Linux: ```sh python -m venv venv```

+ Activate the virtual environment for your current terminal.

  Example (Windows, PowerShell): ```sh venv\Scripts\Activate.ps1``` \
  Example (Linux, bash): ```sh source venv/bin/activate```

  Your command prompt should now start with `(venv)`, this indicates that the virtual environment in `venv` is currently active.


#pagebreak()
= Install the aerial-library
+ Install the aerial-library to your virtual environment.
  Run this command in your shell with the activated venv:
  ```sh
  pip install git+https://github.com/F-WuTS/aerial-library
  ```

+ The Crazyflie client (cfclient) is a tool for configuring Crazyflie drones.
  You can install it to your virtual environment using this command:
  ```sh
  pip install cfclient
  ```


= Enable USB permissions (Linux only)
On Linux, you need to enable USB permissions to enable access to bitcraze products for users other than root.
+ As root, create the file `/etc/udev/rules.d/50-bitcraze.rules` with the following contents:
  // must not have line breaks
  #align(center, block(width: 200%)[
      ```sh
      # Crazyradio (normal operation)
      SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="7777", MODE="0664", TAG+="uaccess"

      # Bootloader
      SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="0101", MODE="0664", TAG+="uaccess"

      # Crazyflie (over USB)
      SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0664", TAG+="uaccess"
      ```
  ])

+ Reboot to apply these rules.
  Alternatively, run this command as root to apply these rules without rebooting:
  ```sh
  udevadm control --reload-rules && udevadm trigger
  ```

Source:
#link("https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/installation/usb_permissions/")[bitcraze documentation],
#link("https://wiki.archlinux.org/title/Udev#Allowing_regular_users_to_use_devices")[ArchWiki]


= Configure the Crazyflie radio address
Every drone in reach of your Crazyradio must have a unique radio address and/or channel, as the drones will not be distinguishable otherwise.
It is therefore recommended to change your Crazyflie's radio address.

+ Power on your Crazyflie and plug the Crazyradio into your computer.
  Make sure your drone is the *only* powered-on drone with that address nearby.

  Alternatively, you can connect the drone via USB cable to your computer and unplug the Crazyradio.
  This way, only the drone connected by cable will be visible.

+ Start the cfclient.
  Enter the radio address of the Crazyflie, by default `E7E7E7E7E7`.
  Click the Scan button to search for available Crazyflie drones nearby.
  Choose your Crazyflie connection from the list and click Connect.

  Once connected, the blue and brown graph in the middle will display the orientation of the drone.
  Try tilting the drone, you should then see the graph moving around respectively.
  The front-left LED of the drone should also be flashing red when data is transferred between your Crazyradio and the drone.

+ Now you can assign a new address to your connected drone.
  In the window menu, open Connect → Configure 2.x.
  In the popup, change the address to a value that is not yet in use by any other drones nearby.
  Click Write, then restart the Crazyflie to apply these changes.

+ Connect to the drone using the new address to verify these changes.


= Crazyflie recovery
In case a drone no longer responds to radio communication or its address is unknown, you can try reinstalling its firmware.
This will reset the Crazyflie to default values, including the radio address.

+ Plug the Crazyradio into your computer and start the cfclient.
  In the window menu, open Connect → Bootloader.

+ In the Cold boot (recovery) tab, select Initiate bootloader cold boot.

+ Now power on the drone to recover by holding down its power button for a few seconnds.
  The rear LEDs of the drone should blink blue now.
  The cfclient will then detect the drone and connect to its bootloader.

+ Select the desired firmware for the Crazyflie, then click Program.
  Wait for the process to finish.

+ Connect to the drone using the default address `E7E7E7E7E7` to verify the recovery.


= Write your first program
Create a new Python script in your project folder.
Example: `my_first_program.py`

Add first instructions to the script:
```py
from aerial_library import Drone, FlowDeck
from time import sleep


with Drone("E7E7E7E7E7", FlowDeck) as drone:
  drone.takeoff(1.0)
  sleep(5)
```

Run your program with the virtual environment active.

Example (Windows): ```sh py my_first_program.py``` \
Example (Linux): ```sh python my_first_program.py```

This program will:
+ Load the required names from the `aerial_library` module and from the built-in `time` module
+ Connect to the drone with address `E7E7E7E7E7`
+ Check that the drone has a flow deck attached, which is required for using motion functions such as `takeoff` and `move_forward`
+ Take off from the ground to an altitude of 1~meter
+ Wait for 5~seconds while the drone is hovering
+ Land automatically because the program has finished running

When something unexpected happens, the program will throw an error.
This could be a problem with the code such as a syntax error,
a problem with the connection such as the wrong address being used,
or it could be anything else as well.
Be sure to read the error message carefully and see which line of your program caused the error.


= Explore available methods
The API documentation for the aerial-library can be found in the downloads section of our website:
https://aerial-challenge.org/downloads/

Check out the `Actions` class for a list of methods available for the connected drone!
