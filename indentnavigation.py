# -*- coding: utf8 -*-

import gi
gi.require_version('Gedit', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, GLib, Gio, Gdk, Gtk, Gedit

from core import navigate


class IndentNavigationViewActivatable(GObject.Object, Gedit.ViewActivatable):

    view = GObject.Property(type=Gedit.View)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self._handlers = [
            self.view.connect('scroll-event', self.on_scroll_event),
            self.view.connect('key-press-event', self.on_key_event),
            self.view.connect('button-press-event', self.on_button_event),
        ]

    def do_deactivate(self):
        for handler in self._handlers:
            self.view.disconnect(handler)

    def on_scroll_event(self, view, event):
        state = event.state & Gtk.accelerator_get_default_mod_mask()

        # Ctrl / Ctrl-Alt is for same or outer
        # Shift-Alt is for outer

        if (state | Gdk.ModifierType.MOD1_MASK) == (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK):
            outer_level = False
        elif state == (Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD1_MASK):
            outer_level = True
        else:
            return False

        if event.delta_y == 0:
            return False

        direction = 1 if event.delta_y > 0 else -1

        navigate(view, direction, outer_level)
        return True

    # this shouldn't exist, maybe replace with acceleators + actions
    def on_key_event(self, view, event):
        # is this mask still needed?
        modifiers = event.state & Gtk.accelerator_get_default_mod_mask()

        # we could use SUPER_MASK, but that's probably not so portable

        # so we use Ctrl-Alt up/down for same-level
        # and Shift-Alt up/down for outer level


        if modifiers == (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK):
            outer_level = False
        elif modifiers == (Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD1_MASK):
            outer_level = True
        else:
            return False

        direction = 1
        may_insert = False

        if event.keyval == Gdk.KEY_Up:
            direction = -1
        elif not outer_level and event.keyval in (Gdk.KEY_Insert, Gdk.KEY_Right):
            may_insert = True
        elif event.keyval != Gdk.KEY_Down:
            return False

        navigate(view, direction, outer_level, may_insert)
        return True

    def on_button_event(self, view, event):
        modifiers = event.state & Gtk.accelerator_get_default_mod_mask()

        if modifiers == (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK):
            outer_level = False
        elif modifiers == (Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD1_MASK):
            outer_level = True
        else:
            return False

        direction = 1
        may_insert = False

        if event.button == 1:
            direction = -1
        elif not outer_level and event.button == 2:
            may_insert = True
        elif event.button != 3:
            return False

        # we get this event before cursor change
        # so we need to compute the target line manually

        _, by = view.window_to_buffer_coords(Gtk.TextWindowType.WIDGET, int(event.x), int(event.y))

        itr, _ = view.get_line_at_y(by)

        navigate(view, direction, outer_level, may_insert, itr=itr)
        return True
