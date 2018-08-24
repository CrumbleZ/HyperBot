import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from extractor import Extractor
from vector import Vector


BALL_SIDE_EPSILON = 0.1


class HyperBot(BaseAgent):

    def initialize_agent(self):
        #This runs once before the bot starts up
        self.controller_state = SimpleControllerState()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        extractor = Extractor(packet, car=packet.game_cars[self.index])

        ball_location = extractor.get_ball_location()
        car_location = extractor.get_my_car_location()
        car_direction = extractor.get_my_car_facing_vector()

        # Determine whether the ball is on the left or the right of where the car is facing
        # Positive value means the ball is to the right, negative is to the left
        ball_side = car_direction.cross3(ball_location - car_location)[2]

        if abs(ball_side) > BALL_SIDE_EPSILON:
            if ball_side > 0:
                turn = 1.0
            else:
                turn = -1.0
        else:
            turn = 0

        self.controller_state.throttle = 1.0
        self.controller_state.steer = turn
        return self.controller_state





        # ball_location = Vector2(packet.game_ball.physics.location.x, packet.game_ball.physics.location.y)
        #
        #
        # my_car = packet.game_cars[self.index]
        # car_location = Vector2(my_car.physics.location.x, my_car.physics.location.y)
        # car_direction = get_car_facing_vector(my_car)
        # car_to_ball = ball_location - car_location
        #
        # steer_correction_radians = car_direction.correction_to(car_to_ball)
        #
        # if steer_correction_radians > 0:
        #     # Positive radians in the unit circle is a turn to the left.
        #     turn = -1.0  # Negative value for a turn to the left.
        # else:
        #     turn = 1.0
        #
        #self.controller_state.throttle = 1.0
        # self.controller_state.steer = turn

        #return self.controller_state


class Vector2:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, val):
        return Vector2(self.x + val.x, self.y + val.y)

    def __sub__(self, val):
        return Vector2(self.x - val.x, self.y - val.y)

    def correction_to(self, ideal):
        # The in-game axes are left handed, so use -x
        current_in_radians = math.atan2(self.y, -self.x)
        ideal_in_radians = math.atan2(ideal.y, -ideal.x)

        correction = ideal_in_radians - current_in_radians

        # Make sure we go the 'short way'
        if abs(correction) > math.pi:
            if correction < 0:
                correction += 2 * math.pi
            else:
                correction -= 2 * math.pi

        return correction


def get_car_facing_vector(car):
    pitch = float(car.physics.rotation.pitch)
    yaw = float(car.physics.rotation.yaw)

    facing_x = math.cos(pitch) * math.cos(yaw)
    facing_y = math.cos(pitch) * math.sin(yaw)

    return Vector2(facing_x, facing_y)
