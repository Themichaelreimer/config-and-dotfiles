# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

import subprocess
import os

PA_MIXER = os.system('pamixer --version') == 0
audio_backend = 'pamixer' if PA_MIXER else 'amixer'

audio_commands = {
        'pamixer': {'up': 'pamixer -i 5', 'down': 'pamixer -d 5', 'mute': 'pamixer -t'},
        'amixer': {'up': 'amixer -D pulse sset Master 5%+', 'down':'amixer -D pulse sset Master 5%-', 'mute': 'amixer -D pulse sset Master 1+ toggle'}
}.get(audio_backend, {})

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["picom", "-b"])
    subprocess.Popen(["xset", "-b"]) # Disables PC Speaker Beeps with audio config
    #subprocess.Popen(["bash", "/home/mike/ultrawide.layout.sh"])
    subprocess.Popen(["xrandr", "--output", "DP-4", "--mode", "3440x1440", "--rate", "100"])

mod = "mod4"
terminal = "/usr/bin/kitty"
font = "CaskaydiaCove Nerd Font Mono"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    #Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Return", lazy.spawn("rofi -show drun"), desc="Show Rofi"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "b", lazy.spawn("/usr/bin/firefox"), desc="Fox!"),
    Key([mod], "t", lazy.spawn("/usr/bin/kitty"), desc="Kitty!"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "control"], "s", lazy.spawn("systemctl suspend"), desc="Suspend session"),
    Key([],"XF86AudioMute", lazy.spawn(audio_commands.get('mute','')), desc="Mute Volume" ),
    Key([],"XF86AudioLowerVolume", lazy.spawn(audio_commands.get('down','')), desc="Lower Volume" ),
    Key([],"XF86AudioRaiseVolume", lazy.spawn(audio_commands.get('up', '')), desc="Raise Volume" ),
    Key([],"XF86MonBrightnessUp", lazy.spawn("brightnessctl s +10%"), desc="Raise Brightness"),
    Key([],"XF86MonBrightnessDown", lazy.spawn("brightnessctl s 10%-"), desc="Lower Brightness")
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# https://docs.qtile.org/en/latest/manual/ref/layouts.html
layouts = [
    layout.Columns(border_focus="#DE1A1B", border_width=4, margin=4),
    layout.Max(margin=4),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    layout.Matrix(margin=4),
    layout.MonadThreeCol(margin=4),
    layout.Spiral(margin=4),
    layout.Floating(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    ]

widget_defaults = dict(
    font="CaskaydiaCove Nerd Font Mono",
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

battery_config = {
    "format": "{char} {percent:2.0%} - {hour:d}:{min:02d}",
    "low_percentage": 0.25,
    "low_background": "#DE1A1B",
    "low_foreground": "#FAD3D4",
    "background": "#417F38",
    "foreground": "#C5E6B4",
    "charge_char": "🗲",
    "discharge_char": "",
    "padding":8
}
groupbox_config = {
    "background":"#056290",
    "active":"#E9F4F9",
    "this_current_screen_border": "#DE1A1B",
    "this_current_screen": "#DE1A1B",
    "inactive": "#04142D"

}

right_arrow = {
    "decorations": [PowerLineDecoration(path="arrow_right")]
}
left_arrow = {
    "decorations": [PowerLineDecoration(path="arrow_left")]
}
screens = [
    Screen(
        wallpaper='~/Pictures/wp.jpeg',
        wallpaper_mode='stretch',
        top=bar.Bar(
            [
                #widget.LaunchBar(),
                #widget.CurrentLayout(background="#0C7CB3", foreground="#E9F4F9", **left_arrow),
                widget.GroupBox(**groupbox_config, **left_arrow),
                widget.Systray(background="#084D71", foreground="#E9F4F9", padding_x=8, **left_arrow),
                widget.Prompt(),
                #widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#da4f56", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Spacer(background="#04142D"),
                widget.Clock(format="%a %B %d %Y %I:%M:%S %p", background="#04142D", foreground="#E9F4F9"),
                widget.Spacer(background="#04142D", **right_arrow),
                widget.Volume(fmt="Vol:{}", background="#0F270F", foreground="#C5E6B4", **right_arrow),
                widget.ThermalSensor(fmt="TEMP:{}", tag_sensor="Tctl", background="#193F1C", foreground="#C5E6B4", foreground_alert="#F55353", **right_arrow),
                widget.CPU(format="CPU:{load_percent}%", background="#215128", foreground="#C5E6B4", **right_arrow),
                widget.Memory(format="MEM:{MemPercent}",background="#2C682C", foreground="#C5E6B4", **right_arrow),
                widget.Battery(**battery_config),
                #widget.QuickExit(background="#04142D"),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        wallpaper='~/Pictures/wp.jpeg',
        wallpaper_mode='stretch',
        top=bar.Bar(
            [
                #widget.LaunchBar(),
                #widget.CurrentLayout(background="#0C7CB3", foreground="#E9F4F9", **left_arrow),
                widget.GroupBox(**groupbox_config, **left_arrow),
                #widget.Systray(background="#084D71", foreground="#E9F4F9", padding_x=8, **left_arrow),
                widget.Prompt(),
                #widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#da4f56", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Spacer(background="#04142D"),
                widget.Clock(format="%a %B %d %Y %I:%M:%S %p", background="#04142D", foreground="#E9F4F9"),
                widget.Spacer(background="#04142D", **right_arrow),
                widget.Volume(fmt="Vol:{}", background="#0F270F", foreground="#C5E6B4", **right_arrow),
                widget.ThermalSensor(fmt="TEMP:{}", tag_sensor="Tctl", background="#193F1C", foreground="#C5E6B4", foreground_alert="#F55353", **right_arrow),
                widget.CPU(format="CPU:{load_percent}%", background="#215128", foreground="#C5E6B4", **right_arrow),
                widget.Memory(format="MEM:{MemPercent}",background="#2C682C", foreground="#C5E6B4", **right_arrow),
                widget.Battery(**battery_config),
                #widget.QuickExit(background="#04142D"),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),

]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
