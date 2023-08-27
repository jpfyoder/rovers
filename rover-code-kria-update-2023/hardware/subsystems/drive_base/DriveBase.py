#!/usr/bin/env python3
""" 
File: DriveBase.py 
 
Description: This file contains the implementation of a DriveBase class that 
extends the DifferentialDrive class. It provides methods for controlling the 
movement of a rover using drive wheels. 
 
Author: Ryan Barry
Date Created: August 12, 2023
"""
import sys

import numpy as np
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import Float32

sys.path.append("../..")
from DifferentialDrive import DifferentialDrive
from DriveWheel import DriveWheel
from RoverConstants import AUTONOMOUS_MODE, WHEEL_NAMES
from RoverPinout import *


class DriveBase(DifferentialDrive, Node):
    def __init__(self, operating_mode):
        DifferentialDrive.__init__(self)
        Node.__init__("drive_base_node")
        self.left_sub = self._create_subscription(
            Float32, "drive_base/left_target_velocity", self.left_callback, 10
        )
        self.right_sub = self._create_subscription(
            Float32, "drive_base/right_target_velocity", self.right_callback, 10
        )
        self.rover_sub = self._create_subscription(
            Twist, "drive_base/target_rover_velocity", self.rover_callback, 10
        )
        self.operating_mode = operating_mode
        self.left_wheels = []
        self.right_wheels = []

        for i in range(len(WHEEL_NAMES)):
            name = WHEEL_NAMES[i]
            pwm_pin = WHEEL_PINS[f"{name}_pwm"]
            wheel = DriveWheel(name=name, pwm_pin=pwm_pin)

            if "left" in name:
                self.left_wheels.append(wheel)
            elif "right" in name:
                self.right_wheels.append(wheel)

    def left_callback(self, msg):
        # Process left target velocity message
        if self.operating_mode == AUTONOMOUS_MODE:
            self.new_target_left_velocity = msg.data

    def right_callback(self, msg):
        # Process right target velocity message
        if self.operating_mode == AUTONOMOUS_MODE:
            self.new_target_right_velocity = msg.data

    def rover_callback(self, msg):
        # Process rover target velocity message
        if self.operating_mode == AUTONOMOUS_MODE:
            x = msg.linear.x
            y = msg.linear.y
            z = msg.linear.z
            w = msg.angular.z
            self.target_velocity = np.array([[x], [y], [z], [w]])

    def set_right_velo(self, velocity):
        for wheel in self.right_wheels:
            wheel.set_velocity(velocity)

    def set_left_velo(self, velocity):
        for wheel in self.left_wheels:
            wheel.set_velocity(velocity)
