import datetime
import sys

class GCode(object):
    _precision = 8
    _axes = ['X', 'Y', 'Z']
    _offset_axes = ['I', 'J']

    def __init__(self, of=None):
        if of is None:
            of = sys.stdout
        self.of = of

    def prologue(self):
        print('(generated via gcode.py; do not edit)', file=self.of)
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'({dt})', file=self.of)
        print('(-- prologue begin --)', file=self.of)
        print('G17 (Use XY plane)', file=self.of)
        print('G20 (Use inch)', file=self.of)
        print('G40 (Cancel cutter radius compensation)', file=self.of)
        print('G49 (Cancel tool length compensation)', file=self.of)
        print('G54 (Default coordinate system)', file=self.of)
        print('G80 (Cancel canned cycle)', file=self.of)
        print('G90 (Use absolute distance mode)', file=self.of)
        print('G94 (Units Per Minute feed rate mode)', file=self.of)
        print('G64 P0.001 (Enable path blending for best speed, with accuracy)', file=self.of)
        print('M3 (Spindle on clockwise)', file=self.of)
        print('(-- prologue end --)', file=self.of)

    def comment(self, s):
        print(f'({s})', file=self.of)

    def goto(self, pos):
        print('G0', self._gen_axes(pos, self._axes))

    def feed(self, rate):
        print(f'F{rate:.{self._precision}f}', file=self.of)

    def move(self, pos):
        print('G1', self._gen_axes(pos, self._axes))

    def circle_ccw(self, end, center_offset):
        print('G3',
            self._gen_axes(end, self._axes),
            self._gen_axes(center_offset, self._offset_axes))

    def epilogue(self):
        print('(-- epilogue begin --)', file=self.of)
        print('M5 (Spindle off)', file=self.of)
        print('M2 (End program)', file=self.of)
        print('(-- epilogue end --)', file=self.of)

    def _gen_axes(self, values, axes):
        values_s = []
        assert len(axes) >= len(values)
        for i in range(len(values)):
            value = values[i]
            if value is None:
                continue
            axis = axes[i]
            values_s.append(f'{axis}{value:.{self._precision}f}')
        return ' '.join(values_s)
