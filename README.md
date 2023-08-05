Clicky colors on a Razer Tartarus V2.

## Simulation

Install Pyglet first (`pip install pyglet`).

```
python colorhand.py pyglet
```

Keymap (you might want to adjust this in source):

main keys on left side of QWERTY (`1`-`5`, `q`-`t`, `a`-`g`, `z`-`v`),
thumb key on `numpad0`,
scroll on `pgup`/`rshift`/`pgdn`,
small button on `rctrl`,
D-pad on arrow keys.

## Raspberry Pi OS installation

- Install [OpenRazer](https://openrazer.github.io/)
- Put this in `~/blinkenhand/`
- Set up autostart:
  ```
  mkdir -p ~/.config/lxsession/LXDE-pi/
  cp /etc/xdg/lxsession/LXDE-pi/autostart ~/.config/lxsession/LXDE-pi/
  echo "@$HOME/blinkenhand/blinkenhand.sh" >> ~/.config/lxsession/LXDE-pi/autostart
  ```
- Install [input-remapper](https://github.com/sezanzeb/input-remapper)
  and set up an all-alphabetic keymap:
  ```
  01 02 03 04 05 -> abcde
  06 07 08 09 10 -> fghij
  11 12 13 14 15 -> klmno
  16 17 18 19    -> pqrs
  small button   -> t
  ← ↑ → ↓        -> uvwx
  scroll up      -> y
  scroll down    -> z
  scrollwheel    -> 1
  20 (big thumb) -> space
  ```
