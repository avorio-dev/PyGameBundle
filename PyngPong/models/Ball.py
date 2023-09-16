####################################################################################################################
# IMPORTS
import math

import pygame.draw


####################################################################################################################
# CORE
class Ball:
    # ---> CONSTANTS
    PPF = 8.5

    # ---> CONSTRUCTOR
    def __init__(self, x, y, radius, color):
        self._def_ball_xy = (x, y)
        self._ball_x = x
        self._ball_y = y
        self._ball_radius = radius
        self._color = color

        self._border = self._ball_radius / 100 * 10
        self._x_vel, self._y_vel = 0, 0

    # ---> FUNCTIONS
    def draw(self, surface):
        pygame.draw.circle(surface,
                           "#000000",
                           center=(self._ball_x, self._ball_y),
                           radius=self._ball_radius)

        pygame.draw.circle(surface,
                           self._color,
                           center=(self._ball_x, self._ball_y),
                           radius=self._ball_radius - self._border)

    def get_surface(self):
        return [self._ball_x, self._ball_y, self._ball_radius]

    def set_velocity(self, x_vel, y_vel):
        self._x_vel = x_vel
        self._y_vel = y_vel

    def move(self):
        self._ball_x += self._x_vel
        self._ball_y += self._y_vel

    def reset_position(self):
        self._ball_x = self._def_ball_xy[0]
        self._ball_y = self._def_ball_xy[1]

    def _get_bounce_angle(self, paddle_x, paddle_y, paddle_width, paddle_height, bf):
        bf_surf = bf.get_surface()
        bf_x, bf_y, bf_width, bf_height = bf_surf[0], bf_surf[1], bf_surf[2], bf_surf[3]

        from_left, from_center, from_right = False, False, False

        # Get previous tick coordinates
        prev_x = self._ball_x - self._x_vel
        prev_y = self._ball_y - self._y_vel

        # Get distances from BF Border to check from what side ball comes from
        prev_dist_from_bf = bf_x + prev_x
        curr_dist_from_bf = bf_x + self._ball_x

        if prev_dist_from_bf < curr_dist_from_bf:
            from_left = True
            print("From Left")

        elif prev_x == self._ball_x:
            from_center = True
            print("From Center")

        elif prev_dist_from_bf > curr_dist_from_bf:
            from_right = True
            print("From Right")

        # If ball comes from center, out angle will be 45 degrees default.
        # If the paddle is on the right side of the battlefield,
        # the ball will go on the left side, and vice-versa
        default_dir = math.radians(45)
        x_vel = math.sin(default_dir) * self.PPF
        y_vel = math.cos(default_dir) * self.PPF
        if paddle_x > bf_x + bf_width / 2:
            x_vel = x_vel * -1

        # Hit Angle Calculation
        # In a right-angled triangle, given the cathetus and the hypotenuse,
        # the angle included will be θ = atan(a / c) (radians).
        # To calculate the length between two points in the Cartesian plane (Cartesian Coordinates),
        # the Euclidean distance formula will be used, which is based on the Pythagorean theorem.
        # Let's suppose we have two points with coordinates (x1, y1) and (x2, y2).
        # The distance between these two points is given by:
        # √[(x2 - x1)² + (y2 - y1)²]
        x1, x2 = self._ball_x, prev_x
        y1, y2 = self._ball_y, prev_y

        len_coming_segment = abs(math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2)))
        len_between_y = abs(prev_y - self._ball_y)

        if len_coming_segment == 0:
            len_coming_segment = 1
        hit_angle_rad = math.atan(len_between_y / len_coming_segment)
        hit_angle_deg = math.degrees(hit_angle_rad)

        # Match Hit Cases
        paddle_center = paddle_x + paddle_width / 2
        if not from_center:
            if self._ball_x == paddle_center:
                x_vel = 0

            elif ((from_right and self._ball_x > paddle_center)
                  or (from_left and self._ball_x < paddle_center)):
                # If the ball hits the same half side which it comes,
                # Out angle will be the complementary angle with which the ball hits the paddle
                # So the ball will be sent on the opposite side of the side it came from
                print("Same Half Side")
                print("Hit Angle -> \t", hit_angle_deg)
                out_angle = 90 - hit_angle_deg
                print("Out Angle -> \t", out_angle)
                out_angle = math.radians(out_angle)
                x_vel = math.sin(out_angle) * self.PPF * -1
                y_vel = math.cos(out_angle) * self.PPF

                if from_left:
                    x_vel = x_vel * -1

            elif ((from_right and self._ball_x < paddle_center)
                  or (from_left and self._ball_x > paddle_center)):
                # If the ball hits the opposite side of the side it came from,
                # Out Angle will be
                # -> If 0 < Hit angle <= 45 Degrees, out angle will be the half complementary angle
                #    which will be 45 < out angle <= 90 degrees
                # -> If 45 > Hit Angle <= 90 Degrees, out angle will be the half complementary angle
                #    which will be 0 < out angle <= 45
                out_angle = 0
                print("Opposite Half Side")
                print("Hit Angle -> \t", hit_angle_deg)
                if 0 <= hit_angle_deg < 45:
                    out_angle = 45 - hit_angle_deg
                elif 45 <= hit_angle_deg <= 90:
                    out_angle = hit_angle_deg - 45
                print("Out Angle -> \t", out_angle)
                out_angle = math.radians(out_angle)
                x_vel = math.sin(out_angle) * self.PPF * -1
                y_vel = math.cos(out_angle) * self.PPF

                if from_right:
                    x_vel = x_vel * -1

        # Set the Y direction based on the upper/bottom side of battlefield.
        # Also, set the current Y position of the ball equal to paddle Y position
        # to avoid that on next tick, the paddle is in the paddle's area yet
        if self._ball_y < bf_height / 2:  # Upper half of battlefield
            y_vel = abs(y_vel)
            self._ball_y = paddle_y + paddle_height + self._ball_radius

        if self._ball_y > bf_height / 2:  # Bottom half of battlefield
            y_vel = abs(y_vel) * -1
            self._ball_y = paddle_y - self._ball_radius

        print("---")
        return [x_vel, y_vel]

    def check_collisions(self, bf, paddle_up, paddle_down):
        collision = False

        # ---> Battlefield collision
        surf = bf.get_surface()
        bf_x, bf_y, bf_width, bf_height = surf[0], surf[1], surf[2], surf[3]

        if self._ball_x <= bf_x + self._ball_radius:
            collision = True
            self._ball_x = bf_x + self._ball_radius
            self.set_velocity(-self._x_vel, self._y_vel)

        if self._ball_x >= bf_x + bf_width - self._ball_radius:
            collision = True
            self._ball_x = bf_x + bf_width - self._ball_radius
            self.set_velocity(-self._x_vel, self._y_vel)

        # ---> Up Paddle Collision
        surf = paddle_up.get_surface()
        pad_x, pad_y, pad_width, pad_height = surf[0], surf[1], surf[2], surf[3]

        if ((pad_x <= self._ball_x <= pad_x + pad_width)
                and (self._ball_y - self._ball_radius <= pad_y + pad_height)):
            collision = True

            velocity = self._get_bounce_angle(pad_x, pad_y, pad_width, pad_height, bf)
            self.set_velocity(velocity[0], velocity[1])

        # ---> Down Paddle Collision
        surf = paddle_down.get_surface()
        pad_x, pad_y, pad_width, pad_height = surf[0], surf[1], surf[2], surf[3]

        if ((pad_x <= self._ball_x <= pad_x + pad_width)
                and (self._ball_y + self._ball_radius >= pad_y)):
            collision = True

            velocity = self._get_bounce_angle(pad_x, pad_y, pad_width, pad_height, bf)
            self.set_velocity(velocity[0], velocity[1])

        return collision

    def check_boundary_cross(self, paddle_up=None, paddle_down=None):
        crossed = False

        if paddle_up:
            surf = paddle_up.get_surface()
            pad_x, pad_y, pad_width, pad_height = surf[0], surf[1], surf[2], surf[3]

            if self._ball_y + self._ball_radius < pad_y + pad_height:
                crossed = True

        if paddle_down:
            surf = paddle_down.get_surface()
            pad_x, pad_y, pad_width, pad_height = surf[0], surf[1], surf[2], surf[3]

            if self._ball_y - self._ball_radius > pad_y:
                crossed = True

        return crossed
