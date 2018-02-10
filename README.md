# Empire at War - Fast Consistent Lasers

This is a Python script which generates a Mod for *Star Wars: Empire at War:
Forces of Corruption*. The goal of this Mod is to make space projectiles faster
and more consistent.

In the base game, lasers and missiles all move pretty slowly, almost
lethargically, like they don't care if they get to their targets before the end
of the battle. Missiles move at the same speed as fighters, or slower, so
fighters flying away from a missile launcher are automatically safe from its
missiles. Additionally, the slow speed of lasers just looks kind of silly, and
some laser types (like the smallest lasers from fighters) travel at different
speeds.

In addition to slow projectile speeds, lasers in the base game come in two
different forms. Small lasers on fighters, corvettes and the heavy lasers on
frigates use a symmetrical 3D model for their projectiles, while turbolasers
appear teardrop-shaped.

This mod aims to fix both these problems, first by increasing projectile speeds
to make them look less lethargic and making all laser-type projectiles move at
the same speed, and second by changing all lasers and turbolasers to either
consistently use symmetrical beam models *or* teardrop shapes (the script has
options for building with either visual type, the speed changes are the same).

## How it Works

Rather than make all the necessary changes manually to implement both mod cases,
the mod is implemented as a Python script which reads in the `projectiles.xml`
config from the "Source" mod that comes with the game (actually just the
un-bundled form of the game's standard XML), and modifies the space projectiles
and writes it out to a new mod in the current directory.

The reason for this is because the mod is changing multiple properties across
many projectiles, so doing it algorithmically makes it much easier to quickly
tune properties of several projectiles. For example, to change the speed that
I set for all lasers, I can change the one place where I set the speed of lasers
and re-run the script, rather than finding every laser in the XML file and
changing it by hand.

## Balance

This is not a balancing mod. I haven't done anything to try to make sure it's
balanced. I mainly made this mod to improve aesthetics of the lasers and other
space projectiles, since I mainly play space skirmish, but don't like how slow
the projectiles seemed to move.

One known balance issue with this mod is that missiles are now faster than
starfighters, so concussion missile launchers are now extremely devastating to
fighter squadrons, even if they turn away as soon as they see missiles incoming.
I currently increase the turning speed of missiles as well as their movement
speeds so their turning radii stay the same, though I may at some point
experiment with giving them larger turning radii to see if it helps balance for
fighters.

## Building the Mod

I will provide a zip file of the mod's built contents in releases, both with
beam-model lasers and with teardrop lasers.

To build the mod yourself, you will need Python 3.6+ and lxml. Clone this
repository into the *Force of Corruption* `Mods` folder:
- `EAWX`
  - `EAWX\Mods`
    - `EAWX\Mods\Source`
    - `EAWX\Mods\eaw-fast-consistent-projectiles`
      - `EAWX\Mods\eaw-fast-consistent-projectiles\make_better_lasers.py`

If the `Source` folder isn't available, you'll need to find or extract a copy of
the game's original `projectiles.xml`.

Run `make_better_lasers.py` in that directory. By default this makes
teardrop-style lasers, but you can set `MAKE_MODEL_BEAMS=True` at the top of the
script to switch which mode it's in. (This isn't a command line argument because
on windows it was easier to edit the script and double-click to run than mess
with what passes for a shell on windows).

## Running the Mod

If you build or unzip the mod files into your *Forces of Corruption* `Mods`
folder, you can then run the mod by passing the modpath to the extracted mod
as an argument to the game.

The easiest way to do this is by making a new shortcut to the game executable
(right-click `swfoc.exe` > copy; right-click > paste shortcut), then go to
properties (right click `swfoc.exe - Shortcut` > properties), and add
` "MODPATH=Mods\eaw-fast-consistent-projectiles"` to the end of the "target"
field.
