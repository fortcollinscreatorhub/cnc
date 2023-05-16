import sys

class ProjectConfig(object):
    def __init__(self, utils):
        # Parametrization
        self.mount_hole_count = 2
        if len(sys.argv) > 1:
            self.mount_hole_count = int(sys.argv[1])

        # Configuration
        self.mount_hole_diam = 0.97
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
        # Clamps are built from this material:
        self.material_thick = 0.750
        # Make sure we cut all the way through the material:
        self.overcut_depth = 0.005
        # Lip should be same thickness as the 1/4" waste board
        # we'll use along with the clamps:
        self.waste_thick = 0.234
        self.lip_depth = -(self.material_thick - self.waste_thick)
        self.bottom_depth = -(self.material_thick + self.overcut_depth)
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
