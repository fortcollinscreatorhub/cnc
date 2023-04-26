#!/usr/bin/env python3

import gcode
import gcode_utils
import project_config

gc = gcode.GCode()
ut = gcode_utils.GCodeUtils(gc)
cfg = project_config.ProjectConfig(ut)

gc.prologue()
ut.safe_z()

for n in range(cfg.mount_hole_count):
    gc.comment(f'Mounting hole {n}')
    mount_cx = cfg.hole_0_x + (n * cfg.mount_hole_spacing)
    ut.pocket_cylinder(
        [mount_cx, cfg.hole_y],
        cfg.mount_hole_radius - cfg.bit_radius,
        cfg.bottom_depth)
    if n != (cfg.mount_hole_count - 1):
        gc.comment(f'Screw hole {n}')
        screw_cx = mount_cx + (cfg.mount_hole_spacing / 2)
        ut.pocket_cylinder(
            [screw_cx, cfg.hole_y],
            cfg.screw_hole_radius - cfg.bit_radius,
            cfg.bottom_depth)

gc.comment('Lip pocket')
ut.pocket_cuboid(
    cfg.bit_radius, # major_min
    cfg.bit_radius + cfg.x_total, # major_max
    cfg.bit_radius + cfg.lip_y_min + cfg.bit_radius, # minor_min
    cfg.bit_radius + cfg.y_total, # minor_max
    cfg.lip_depth, # depth
    0 # vec_major_index
)

gc.comment('Profile')
ut.profile_polyline(
    [
        # [
        #     [
        #         line start x,
        #         line start y,
        #     ],
        #     [[tab percent, length]...]
        # ]
        [
            [
                0,
                0
            ],
            []
        ],
        [
            [
                cfg.bit_radius + cfg.x_total + cfg.bit_radius,
                0,
            ],
            [[0.5, cfg.tab_length]]
        ],
        [
            [
                cfg.bit_radius + cfg.x_total + cfg.bit_radius,
                cfg.bit_radius + cfg.y_total + cfg.bit_radius
            ],
            [[0.7, cfg.tab_length]]
        ],
        [
            [
                0,
                cfg.bit_radius + cfg.y_total + cfg.bit_radius
            ],
            []
        ],
        [
            [
                0,
                0,
            ],
            [[0.3, cfg.tab_length]]
        ]
    ],
    cfg.bottom_depth
)

gc.comment('Safe')
ut.safe_z()

gc.epilogue()
