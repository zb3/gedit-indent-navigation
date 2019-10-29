# gedit-indent-navigation

This is plugin adds the following bindings:
<table>
  <tr>
    <td style="white-space: nowrap;"><kbd>Ctrl</kbd> + Scroll&nbsp;Up/Down<br>
    <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>Up</kbd> / <kbd>Down</kbd><br>
    <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + Left/Right click
  <td>Jump to the previous/next line with the same or lower (whichever occurs first) indentation level as the current line.
  <tr>
    <td style="white-space: nowrap;"><kbd>Shift</kbd> + <kbd>Alt</kbd> + Scroll&nbsp;Up/Down<br>
    <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>Up</kbd> / <kbd>Down</kbd><br>
    <kbd>Shift</kbd> + <kbd>Alt</kbd> + Left/Right click
    <td>Jump to the previous/next line with an indentation level lower than the current line. 
</table>

* Empty lines and lines containing only indentation characters are skipped.
* Mouse click changes the current line before jumping.
* If something was selected, these jumps extend the selection.

### Disclaimer
This plugin is experimental and its behaviour may change (fork advised).

## Installation
1. Make sure your gedit version is up to date.
2. Copy project folder to `~/.local/share/gedit/plugins`
3. Enable `Indent Navigation` plugin.
4. That's it :)
