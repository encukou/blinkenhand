import sys
import numpy
rng = numpy.random.default_rng()
colors = numpy.zeros((4, 6, 3), dtype=int)
print(colors)
COLORS = (
    (0, 0, 0),
    #(0x9e, 0x42, 0x44),
    (228, 3, 3),
    (255, 140, 0),
    (255, 237, 0),
    (0, 255, 38*2),
    (36*2, 64*2, 255),
    (115*2, 41*2, 255),
    (0xf6, 0x99, 0xcd),
    (255, 255, 255),
)
NEXT_COLOR = {c: n for c, n in zip(COLORS, (*COLORS[1:], COLORS[0]))}

COORDS = {
    'a': (0, 0),
    'b': (0, 1),
    'c': (0, 2),
    'd': (0, 3),
    'e': (0, 4),
    'f': (1, 0),
    'g': (1, 1),
    'h': (1, 2),
    'i': (1, 3),
    'j': (1, 4),
    'k': (2, 0),
    'l': (2, 1),
    'm': (2, 2),
    'n': (2, 3),
    'o': (2, 4),
    'p': (3, 0),
    'q': (3, 1),
    'r': (3, 2),
    's': (3, 3),
    '1': (3, 4),
    ' ': (3, 5),
}

def handle_keypress(key):
    coords = COORDS.get(key)
    if coords:
        now = tuple(colors[coords])
        nxt = NEXT_COLOR.get(now, (0, 0, 0))
        colors[coords] = nxt
    elif key == 't':
        colors[:] = rng.choice(COLORS[1:], size=colors.shape[:2])
    elif key == 'u':
        colors[:, :-1] = numpy.roll(colors[:, :-1], -1, 1)
    elif key == 'v':
        colors[:, :-1] = numpy.roll(colors[:, :-1], -1, 0)
    elif key == 'w':
        colors[:, :-1] = numpy.roll(colors[:, :-1], 1, 1)
    elif key == 'x':
        colors[:, :-1] = numpy.roll(colors[:, :-1], 1, 0)
    elif key == 'y':
        for i, row in enumerate(colors):
            for j, c in enumerate(row):
                try:
                    idx = COLORS.index(tuple(c))
                except ValueError:
                    idx = 0
                if idx > 0:
                    idx -= 1
                colors[i, j] = COLORS[idx]
    elif key == 'z':
        for i, row in enumerate(colors):
            for j, c in enumerate(row):
                try:
                    idx = COLORS.index(tuple(c))
                except ValueError:
                    idx = 0
                if 0 < idx < len(COLORS) - 1:
                    idx += 1
                colors[i, j] = COLORS[idx]
    refresh()


if sys.argv[1:2] == ['pyglet']:
    import pyglet
    window = pyglet.window.Window()

    W = H = 100
    batch = pyglet.graphics.Batch()
    rects = [
        [
            pyglet.shapes.Rectangle(
                y=window.height-(i+1)*W,
                x=j*H,
                width=W-1,
                height=H-1,
                batch=batch,
                color=(0,0,0),
            )
            for j in range(colors.shape[1])
        ]
        for i in range(colors.shape[0])
    ]
    for i in range(colors.shape[0]-1):
        rects[i][5].width = 0
    rects[3][4].width /= 5
    rects[3][4].x += W * 2/5
    rects[3][5].height += H / 2
    rects[3][5].y -= H / 2
    rects[3][5].rotation = 30

    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    @window.event
    def on_key_press(key, mod):
        k = {
            pyglet.window.key._1: 'a',
            pyglet.window.key._2: 'b',
            pyglet.window.key._3: 'c',
            pyglet.window.key._4: 'd',
            pyglet.window.key._5: 'e',
            pyglet.window.key.Q: 'f',
            pyglet.window.key.W: 'g',
            pyglet.window.key.E: 'h',
            pyglet.window.key.R: 'i',
            pyglet.window.key.T: 'j',
            pyglet.window.key.A: 'k',
            pyglet.window.key.S: 'l',
            pyglet.window.key.D: 'm',
            pyglet.window.key.F: 'n',
            pyglet.window.key.G: 'o',
            pyglet.window.key.Z: 'p',
            pyglet.window.key.X: 'q',
            pyglet.window.key.C: 'r',
            pyglet.window.key.V: 's',

            pyglet.window.key.RCTRL: 't',
            pyglet.window.key.LEFT: 'u',
            pyglet.window.key.UP: 'v',
            pyglet.window.key.RIGHT: 'w',
            pyglet.window.key.DOWN: 'x',
            pyglet.window.key.PAGEUP: 'y',
            pyglet.window.key.PAGEDOWN: 'z',
            pyglet.window.key.RSHIFT: '1',
            pyglet.window.key.NUM_0: ' ',
        }.get(key)
        if k:
            handle_keypress(k)

    def refresh():
        print(colors)
        for i, row in enumerate(colors):
            for j, c in enumerate(row):
                rects[i][j].color = c

    pyglet.app.run()
else:
    import sys, os, tty, termios
    from openrazer.client import DeviceManager

    def readchar(stream=sys.stdin):
        fd = stream.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return os.read(fd, 1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    manager = DeviceManager()
    device = manager.devices[0]
    device.brightness = 100

    def refresh():
        for i, row in enumerate(colors):
            for j, c in enumerate(row):
                device.fx.advanced.matrix.set(i, j, tuple(c))
        device.fx.advanced.draw()

    refresh()
    while (c := readchar()) not in b'\x1b\x7f=':
        handle_keypress(c.decode())
        print('press Esc, Backspace or `=` to quit')
