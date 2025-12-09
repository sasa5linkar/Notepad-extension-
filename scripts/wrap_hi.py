# -*- coding: utf-8 -*-
"""
Notepad++ PythonScript - Wrap selected text in <hi> tag
"""

# Get the selected text
selected_text = editor.getSelText()

if selected_text:
    # Wrap the selected text with <hi> tags
    wrapped_text = "<hi>" + selected_text + "</hi>"
    
    # Replace the selection with the wrapped text
    editor.replaceSel(wrapped_text)
else:
    # If no text is selected, insert empty tags and position cursor between them
    editor.replaceSel("<hi></hi>")
    # Move cursor back 5 positions (length of "</hi>")
    current_pos = editor.getCurrentPos()
    editor.setCurrentPos(current_pos - 5)
    editor.setSelection(current_pos - 5, current_pos - 5)
