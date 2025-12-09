# -*- coding: utf-8 -*-
"""
Notepad++ PythonScript - Wrap selected text in <head> tag
"""

# Get the selected text
selected_text = editor.getSelText()

if selected_text:
    # Wrap the selected text with <head> tags
    wrapped_text = "<head>" + selected_text + "</head>"
    
    # Replace the selection with the wrapped text
    editor.replaceSel(wrapped_text)
else:
    # If no text is selected, insert empty tags and position cursor between them
    editor.replaceSel("<head></head>")
    # Move cursor back 7 positions (length of "</head>")
    current_pos = editor.getCurrentPos()
    editor.setCurrentPos(current_pos - 7)
    editor.setSelection(current_pos - 7, current_pos - 7)
