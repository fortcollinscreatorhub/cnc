import math

class GCodeUtils(object):
    def __init__(self, gc):
        self.gc = gc

        self.near_depth = 1.0
        self.safe_depth = 1.0
        self.feed_move = 1.0
        self.feed_plunge = 1.0
        self.step_z = 0.1
        self.step_xy = 0.1

    def near_z_dn(self):
        self.gc.goto([None, None, self.near_depth])

    def near_z_up(self):
        self.gc.move([None, None, self.near_depth])

    def safe_z(self):
        self.gc.goto([None, None, self.safe_depth])

    def safe_z_up(self):
        self.near_z_up()
        self.safe_z()

    # No bit diameter compensation is performed
    def pocket_cylinder(self, center, radius, depth):
        zs = self._gen_steps(depth, -self.step_z)
        rs = self._gen_steps(radius, self.step_xy)

        self.gc.goto(center)
        self.near_z_dn()

        for z in zs:
            self.gc.feed(self.feed_move)
            self.gc.move(center)

            self.gc.feed(self.feed_plunge)
            self.gc.move([None, None, z])
            self.gc.feed(self.feed_move)

            for r in rs:
                pos = [center[0] + r, center[1], None]
                self.gc.move(pos)
                self.gc.circle_ccw(pos, [-r, 0])

        self.safe_z_up()

    # No bit diameter compensation is performed
    # vec_major_index == 0 -> long cuts along x
    # vec_major_index == 1 -> long cuts along y
    def pocket_cuboid(self,
        major_min, major_max,
        minor_min, minor_max,
        depth, vec_major_index
    ):
        minor_delta = minor_max - minor_min
        minor_offsets = self._gen_steps(minor_delta, self.step_xy)
        zs = self._gen_steps(depth, -self.step_z)
        vec_minor_index = 1 - vec_major_index
        parity = 0

        dest = [None, None, None]
        dest[vec_major_index] = major_min
        dest[vec_minor_index] = minor_min
        self.gc.goto(dest)
        self.near_z_dn()

        for z in zs:
            dest = [None, None, None]
            dest[vec_major_index] = major_min
            dest[vec_minor_index] = minor_min
            self.gc.goto(dest)

            self.gc.feed(self.feed_plunge)
            self.gc.move([None, None, z])
            self.gc.feed(self.feed_move)

            dest = [None, None, None]
            dest[vec_major_index] = major_max
            self.gc.move(dest)

            parity = False
            for offset in minor_offsets:
                if parity:
                    major = major_max
                else:
                    major = major_min
                parity = not parity

                dest = [None, None, None]
                dest[vec_minor_index] = minor_min + offset
                self.gc.move(dest)

                dest = [None, None, None]
                dest[vec_major_index] = major
                self.gc.move(dest)

        self.safe_z_up()

    # No bit diameter compensation is performed
    def profile_polyline(self, segments, depth):
        zs = self._gen_steps(depth + self.step_z, -self.step_z)

        segment0 = segments[0]
        coord0 = segment0[0]

        # Goto initial corner
        self.gc.goto(coord0)
        self.near_z_dn()

        # All layers without tabs
        for z in zs:
            self.gc.feed(self.feed_plunge)
            self.gc.move([None, None, z])
            self.gc.feed(self.feed_move)

            for segment in segments:
                coord = segment[0]
                self.gc.move(coord)

            self.gc.move(coord0)

        # Last layer with tabs
        self.gc.feed(self.feed_plunge)
        self.gc.move([None, None, depth])
        self.gc.feed(self.feed_move)

        coord_cur = coord0
        first = True
        for segment in segments:
            if first:
                first = False
                continue

            coord_next = segment[0]
            edge_vec = self._vec_sub_vec(coord_next, coord_cur)
            edge_len = self._vec_length(edge_vec)

            for tab in segment[1]:
                [tab_pct, tab_len] = tab
                tab_len_side = tab_len / 2
                tab_proportion_side = tab_len_side / edge_len
                tab_vec_side = \
                    self._vec_mul_scalar(edge_vec, tab_proportion_side)
                tab_center = self._vec_add_vec(
                    coord_cur,
                    self._vec_mul_scalar(edge_vec, tab_pct))
                up = self._vec_sub_vec(tab_center, tab_vec_side)
                dn = self._vec_add_vec(tab_center, tab_vec_side)

                self.gc.move(up)
                self.gc.feed(self.feed_plunge)
                self.gc.move([None, None, depth + self.step_z])
                self.gc.feed(self.feed_move)
                self.gc.move(dn)
                self.gc.feed(self.feed_plunge)
                self.gc.move([None, None, depth])
                self.gc.feed(self.feed_move)

            self.gc.move(coord_next)
            coord_cur = coord_next

        self.gc.move(coord0)
        self.safe_z_up()

    def _gen_steps(self, end, step):
        if end < 0:
            sign = -1
            end *= sign
            step *= sign
        else:
            sign = 1

        vals = []
        cur = end
        while cur > 0.00000001:
            vals.append(sign * cur)
            cur -= step
        return list(reversed(vals))

    def _vec_add_vec(self, vec1, vec2):
        result = []
        for ix in range(len(vec1)):
            v1 = vec1[ix]
            v2 = vec2[ix]
            if v1 is None and v2 is None:
                result.append(None)
            else:
                if v1 is None:
                    v1 = 0
                if v2 is None:
                    v2 = 0
                result.append(v1 + v2)
        return result

    def _vec_sub_vec(self, vec1, vec2):
        result = []
        for ix in range(len(vec1)):
            v1 = vec1[ix]
            v2 = vec2[ix]
            if v1 is None and v2 is None:
                result.append(None)
            else:
                if v1 is None:
                    v1 = 0
                if v2 is None:
                    v2 = 0
                result.append(v1 - v2)
        return result

    def _vec_mul_scalar(self, vec, scalar):
        result = []
        for val in vec:
            if val is None:
                result.append(None)
            else:
                result.append(val * scalar)
        return result

    def _vec_length(self, vec):
        sum = 0
        for val in vec:
            if val is None:
                continue
            sum += val * val
        return math.sqrt(sum)
