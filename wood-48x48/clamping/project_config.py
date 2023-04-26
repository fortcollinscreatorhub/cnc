import sys

class ProjectConfig(object):
    def __init__(self, utils):
        # Parametrization
        self.mount_hole_count = 2
        if len(sys.argv) > 1:
            self.mount_hole_count = int(sys.argv[1])

        # Configuration
        self.mount_hole_diam = 1.0
        self.screw_hole_diam = 0.5
        self.corner_hole_diam = 0.5
        self.margin_side = 1.0
        self.margin_back = 1.0
        self.margin_front = 0.5
        self.mount_hole_spacing = 4
        self.lip_size = 0.5
        self.bit_diam = 0.25
        self.step_xy = self.bit_diam / 2
        self.step_z = 0.1
        self.safe_depth = 1.0
        self.near_depth = 0.1
        self.lip_depth = -0.5
        self.bottom_depth = -0.75
        self.feed_move = 30
        self.feed_plunge = 10
        self.tab_length = 0.1

        # Internal calculations
        self.bit_radius = self.bit_diam / 2
        self.mount_hole_radius = self.mount_hole_diam / 2
        self.screw_hole_radius = self.screw_hole_diam / 2
        self.corner_hole_radius = self.corner_hole_diam / 2
        self.x_total = self.margin_side + self.mount_hole_radius + ((self.mount_hole_count - 1) * self.mount_hole_spacing) + self.mount_hole_radius + self.margin_side
        self.lip_y_min = self.margin_back + self.mount_hole_diam + self.margin_front 
        self.y_total = self.lip_y_min + self.lip_size
        self.hole_0_x = self.bit_radius + self.margin_side + self.mount_hole_radius
        self.hole_y = self.bit_radius + self.margin_back + self.mount_hole_radius
        self.tab_length += self.bit_diam

        utils.near_depth = self.near_depth
        utils.safe_depth = self.safe_depth
        utils.feed_move = self.feed_move
        utils.feed_plunge = self.feed_plunge
        utils.step_z = self.step_z
        utils.step_xy = self.step_xy
