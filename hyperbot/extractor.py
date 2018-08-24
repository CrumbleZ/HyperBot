#######################################################
# EXTRACTOR FUNCTIONS
# Functions that are designed to extract information
# from a GameTickPacket in a less verbose fashion
#######################################################

import math

from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.game_data_struct import PlayerInfo
from vector import Vector



class Extractor:

    def __init__(self, packet: GameTickPacket, car):
        self._packet = packet
        self._car = car

    def get_ball_location(self) -> Vector:
        """Gives the location of the ball as a vector3"""
        return Vector(self._packet.game_ball.physics.location.x,
                      self._packet.game_ball.physics.location.y,
                      self._packet.game_ball.physics.location.z)

    def get_my_car_location(self) -> Vector:
        """Gives the location of the bot's car as a vector3"""
        return self.get_car_location(self._car)

    def get_my_car_facing_vector(self) -> Vector:
        """Gives a unit vector indicating which directon the bot's car is facing as a vector3"""
        return self.get_car_facing_vector(self._car)

    def get_my_team(self):
        return self._car.team


    @staticmethod
    def get_car_location(car: PlayerInfo) -> Vector:
        """Gives the location of given car as a vector3"""
        return Vector(car.physics.location.x,
                      car.physics.location.y,
                      car.physics.location.z)

    @staticmethod
    def get_car_facing_vector(car: PlayerInfo) -> Vector:
        """Gives a unit vector indicating which directon the given car is facing as a vector3"""
        pitch = float(car.physics.rotation.pitch)
        yaw = float(car.physics.rotation.yaw)

        return Vector(math.cos(yaw) * math.cos(pitch),
                      math.sin(yaw) * math.cos(pitch),
                      math.sin(pitch))