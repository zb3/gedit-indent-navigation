def navigate(view, direction, outer_level=False, may_insert=False, itr=None):
    buff = view.get_buffer()

    if itr is None:
        itr = buff.get_iter_at_mark(buff.get_insert())

    orig_y, _ = view.get_line_yrange(itr)

    has_selection = buff.get_has_selection()

    itr = navigate_iter(buff, itr, direction, outer_level, may_insert)

    if has_selection:
        buff.move_mark_by_name('insert', itr)
    else:
        buff.place_cursor(itr)

    new_y, _ = view.get_line_yrange(itr)

    vadj = view.get_vadjustment()
    vadj.set_value(vadj.get_value() + new_y - orig_y)

def navigate_iter(buffer, itr, direction=1, outer_level=False, may_insert=False):
    base_line = line = itr.get_line()

    base_level, _, _ = get_indent_level(buffer, line, skip_empty_line=False)
    total_lines = buffer.get_line_count()
    level = -1

    while True:
        line += direction
        if line < 0 or line >= total_lines:
            break

        level, itr, _ = get_indent_level(buffer, line)
        if level == -1:
            continue

        if level < base_level or (not outer_level and level == base_level):
            break

    if may_insert:
        if level < base_level:
            while True:
                line -= direction
                level, itr, line_empty = get_indent_level(buffer, line, skip_empty_line=False)

                if line == base_line:
                    level = -1
                    break

                if not line_empty or level == base_level:
                    break

        if level != base_level:
            itr = insert_indent(buffer, itr, base_line)

    return itr

def insert_indent(buffer, itr, tpl_line):
    tpl_start = buffer.get_iter_at_line(tpl_line)
    _, tpl_indent_end, _ = get_indent_level(buffer, tpl_line, skip_empty_line=False)
    indent = tpl_start.get_text(tpl_indent_end)

    # move itr to the end of this line
    while True:
        ch = itr.get_char()
        if ch in ('', '\r', '\n'):
            break
        itr.forward_char()

    buffer.begin_user_action()
    buffer.insert(itr, '\n'+indent)
    buffer.end_user_action()

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

    is_empty = ch in ('\r', '\n', '')
    if skip_empty_line and is_empty:
        # this line had only indent, so its level doesn't matter
        level = -1

    return level, itr, is_empty

