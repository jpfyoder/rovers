'''
File: Rover.py

Description:This file defines the "Rover" class, which represents 
the main hardware and functionalities of the rover. It acts as an 
interface between the rover's missions and its various subsystems. 
The class handles the initialization of the rover's status, peripherals, 
and subsystems, as well as updating the LEDs based on the rover's status.

Author: Ryan Barry
Date Created: July 16, 2023
'''

import rclpy
from RoverConstants import *
from hardware.RoverStatus import RoverStatus
from subsystems.arm.ArmRobot import ArmRobot
from sensors.Camera import Camera
from peripherals.LED import LED


class Rover:
    def __init__(self):
        # Initialize Status
        self.status = RoverStatus()
        self.active_mission = EXTREME_RETRIEVAL_DELIVERY

        # Initialize Peripherals
        self.arm = ArmRobot()
        self.operating_mode_LED = LED(color=BLUE)
        self.comm_link_LED = LED()
        self.waypoint_LED = LED()

    def update_LEDs(self):
        if self.status.operating_mode == DRIVER_CONTROL_MODE:
            self.operating_mode_LED.set_color(BLUE)
        elif self.status.operating_mode == AUTONOMOUS_MODE:
            self.operating_mode_LED.set_color(RED)
        # Add code to set the operating mode LED color

        if self.status.comm_link_status == CONNECTED:
            pass
        elif self.status.comm_link_status == NOT_CONNECTED:
            pass

        if self.status.waypoint_status == WAYPOINT_COMPLETE:
            self.waypoint_LED.set_color(GREEN)
            # Add code to set waypoint LED

    def run(self):
        rclpy.spin(self.status)  # Spin the RoverStatus node
        rclpy.spin(self.arm)  # Spin the ArmRobot node

        self.status.destroy_node()
        self.arm.destroy_node()
