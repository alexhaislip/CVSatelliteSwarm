## Unnamed Project

The goal of this project is to control a swarm of cheap robots from an overhead
camera.

The robots regularly recieve positional data from the overhead camera via radio transmissions. The
Camera will use OpenCV to track the robots position and rotation, and assigns targets.

In an effort to keep this project as simple as possible, the robots are
made from preassembled boards that can be bought cheaply online.

This will probably be the list of components per robot:
 - USB charging circuit
 - Lithium Battery
 - 5V Boost DC-DC Converter
 - 433MHz ISM radio reciever module
 - Tiny stepper motors with included driver
 - Arduino Pro Mini
