def navigate(view, direction, outer_level=False, itr=None):
    buff = view.get_buffer()

    if itr is None:
        itr = buff.get_iter_at_mark(buff.get_insert())

    orig_y, _ = view.get_line_yrange(itr)

    has_selection = buff.get_has_selection()

    itr = navigate_iter(buff, itr, direction, outer_level)

    if has_selection:
        buff.move_mark_by_name('insert', itr)
    else:
        buff.place_cursor(itr)

    new_y, _ = view.get_line_yrange(itr)

    vadj = view.get_vadjustment()
    vadj.set_value(vadj.get_value() + new_y - orig_y)


def navigate_iter(buffer, itr, direction=1, outer_level=False):
    line = itr.get_line()

    base_level, _ = get_indent_level(buffer, line, skip_empty_line=False)
    total_lines = buffer.get_line_count()

    while True:
        line = line + direction
        if line < 0 or line >= total_lines:
            break

        level, itr = get_indent_level(buffer, line)
        if level == -1:
            continue

        if level < base_level or (not outer_level and level == base_level):
            break

    return itr


def get_indent_level(buffer, line, skip_empty_line=True):
    itr = buffer.get_iter_at_line(line)
    level = 0

    while True:
        ch = itr.get_char()

        if ch not in (' ', '\t'):
            break

        level += 1
        itr.forward_char()

    if skip_empty_line and ch in ('\r', '\n', ''):
        # this line had only indent, so its level doesn't matter
        level = -1

    return level, itr
