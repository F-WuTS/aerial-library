
#set page(
    paper: "a4",
    numbering: "1/1",
    header: [
        #set align(center)
        #show text: smallcaps

        Getting started with the aerial-library
    ]
)

#set par(justify: true)
#set text(lang: "en")

#show heading: it => v(1em) + it
#show link: underline

#let code_dist = 3pt
#show raw: it => box(
    fill: luma(240),
    inset: (left: code_dist, right: code_dist),
    outset: (top: code_dist, bottom: code_dist),
    radius: 1pt,
    text(0.95em, it)
)

#show "PROJECT": "[...]/aerial-competition"

== What you need
- bitcraze STEM drone bundle
  - Crazyflie 2.x
  - Flow deck v2
  - Crazyradio 2.0
- Laptop or other computer
  - USB port (type A)
  - Python


== Assemble the drone
Complete the drone assembly according to the official guide: \
https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyflie-2-x/#assembling.


== Set up a development environment
Since you should not install Python libraries directly to your computer, set up a so-called virtual environment first.

+ Create a folder *somewhere* on your computer.

  Example (Windows): `C:\Users\YOU\Documents\aerial-competition` \
  Example (Linux): `/home/YOU/Documents/aerial-competition`

  In the following steps, this folder will be referred to as `PROJECT`.

+ Open a terminal and navigate to `PROJECT`.

+ Create the virtual environment for installing Python libraries.

  In `PROJECT`, invoke the python module "venv" and call the target folder for the virtual environment "venv".

  Windows: `py -m venv venv` \
  Linux: `python -m venv venv`

+ Activate the virtual environment.
  This step needs to be *repeated* every time you open a *new* terminal window or tab!

  Run/source the corresponding activation script for your shell in `PROJECT`.
  See the table in the official documentation for which script is the right one for you: \
  https://docs.python.org/3/library/venv.html#how-venvs-work

  Example (Windows, PowerShell): `venv\Scripts\Activate.ps1` \
  Example (Linux, bash): `source venv/bin/activate`

  Your command prompt should now start with `(venv)`, this indicates that the virtual environment in `venv` is currently active.


#pagebreak()
== Install the aerial-library
+ Install the aerial-library to your virtual environment.

  Run this command in your shell with the activated virtual environment: \
  `pip install git+https://github.com/F-WuTS/aerial-library`

+ Install the Crazyflie client to your virtual environment.
  This will be needed for configuring the radio connection between your computer and the drone.

  Run this command in your shell with the activated virtual environment: \
  `pip install cfclient`


== Configure the radio connection
+ Power on your Crazyflie and plug the Crazyradio into your computer.

+ Linux only: Enable USB permissions for bitcraze products.

  #let note = footnote[
      See
      #link("https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/installation/usb_permissions/")[bitcraze documentation],
      #link("https://wiki.archlinux.org/title/Udev#Allowing_regular_users_to_use_devices")[ArchWiki]
  ]
  Create the file `/etc/udev/rules.d/50-bitcraze.rules` as *superuser* with the following contents #note:

  // must not have line breaks
  #align(center, block(width: 200%)[
      ```
      # Crazyradio (normal operation)
      SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="7777", MODE="0664", TAG+="uaccess"

      # Bootloader
      SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="0101", MODE="0664", TAG+="uaccess"

      # Crazyflie (over USB)
      SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0664", TAG+="uaccess"
      ```
  ])

  Example (nano):
  - Copy file contents
  - Run `sudo nano /etc/udev/rules.d/50-bitcraze.rules`
  - Ctrl+Shift+V to paste clipboard
  - Ctrl+X to exit, Y to confirm save operation, Enter to confirm name

  Then, run `sudo udevadm control --reload-rules && sudo udevadm trigger` to apply these rules.

+ Start the Crazyflie client and connect to your drone.

  First, make sure this is the *only* powered-on drone nearby!
  The client may otherwise not be able to distinguish between the drones.

  With your virtual environment active, run `cfclient`.
  Click the Scan button to search for available Crazyflie drones nearby.
  By default, a new Crazyflie is available as `radio://0/80/2M`.
  Select this connection and click the Connect button.

  The blue and brown graph in the middle should now display the orientation of the drone -- try tilting the drone!
  The front left LED of the drone should also be flashing red as data is transferred between your Crazyradio and the drone.

+ Set up the Crazyflie's radio channel.

  In the window menu, open Connect → Configure 2.x.

  --- TODO: assign channels? use addresses? ---

  Change the radio channel to a number that is not yet in use by any other drones nearby and write these changes.
  Restart the Crazyflie to use the new radio channel.
  Connect to the drone on the new channel to confirm the changes.


== Write your first program
+ Create a Python file.

  In `PROJECT`, create a new file ending in `.py` and open it with the text editor of your choice.

  Example: `my_first_program.py`

+ Add first instructions to the script:
  ```py
  from aerial_library import Drone


  with Drone() as drone:
      drone.takeoff()
      drone.land()
  ```

+ Run your program with the virtual environment active.

  Example (Windows): `py my_first_program.py` \
  Example (Linux): `python my_first_program.py`

  If only one Crazyflie is available, the library will automatically connect to that one for you.
  If multiple connections are available, you need to choose between the available connections by entering the corresponding number.

+ Explore the available methods:

  --- TODO where doc ---
