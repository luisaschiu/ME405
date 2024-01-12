# Term Project Proposal

## Description

Our pen plotter project will use a cylindrical axis system, and it involves a radial arm that rotates around a hub and a lead screw that moves the pen 
radially. One motor will rotate the hub, which will rotate the radial arm, and another motor will rotate the lead screw. The nut in the lead screw 
will ideally be translating linearly and not rotating. To prevent the pen from rotating, we will incorporate a slider mechanism below the lead screw. 
We will create a 3-D printed part that acts as the pen carrier, connecting the slider mechanism's moving tab and the lead screw nut. We plan to 3-D 
print a mount to keep both motors stationed at the origin (which we will define as the top-middle position of the paper). For the radial arm, we will 
have a drive shaft connected to the rotating hub. The other end of the drive shaft will be connected to a wheel that will assist in the rotation of 
the radial arm. There will be a 3-D printed support wheel attached to the end of the slider and lead screw combination to prevent system failure 
from the weight of the components similar to cantilever beam deflection.

To move the pen vertically, we will be using a solenoid. The solenoid will control the pen's vertical displacement and control whether or not the pen 
is making contact with the paper. The motors and the solenoid will be controlled using the Nucleo L476 development board and Shoe provided by 
the ME405 Tub. 

***NOTE: The solenoid and Sharpie pen are not pictured in the CAD assembly below, but will be incorporated later.

## Bill of Materials

| Qty. | Part                     | Source                | Est. Cost |
|:----:|:-------------------------|:----------------------|:---------:|
|  2   | Pittperson Gearmotors    | ME405 Tub             |     -     |
|  1   | Nucleo with Shoe         | ME405 Tub             |     -     |
|  1   | Black  Sharpie&trade;    | Home                  |     -     |
|  2   | Motor Mount Parts        | Innovation Sandbox    |     -     |
|  1   | Pen Carrier              | Innovation Sandbox    |     -     |
|  1   | Support Wheel            | Innovation Sandbox    |     -     |
|  1   | Solenoid                 | Digikey               |   $4.95   |
|  1   | T-Slot Framing Extrusion | Mc-Master Carr        |   $2.88   |
|  1   | Lead Screw               | Home Depot            |   $1.71   |
|  2   | Bearings                 | Home Depot            |   $8.00   |
|  1   | Drive Shaft              | Home Depot            |   $8.40   |
|  2   | Drive Shaft Coupling     | ?                     |     ?     |
|  1   | Driving Wheel            | ?                     |     ?     |
|  1   | Main Shaft (at base)     | ?                     |     ?     |


The last three parts are undetermined at this time because they are either too expensive or we are still looking into other options at this time. 
We are considering manufacturing these parts in the machine shops.


## Scaled Sketches of Proposed System

![alt text](Fixture_1.png)
Figure 1. Isometric Front View

![alt text](Fixture_2.png)
Figure 2. Isometric Back View