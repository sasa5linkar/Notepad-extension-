# -*- coding: utf-8 -*-
"""
Notepad++ PythonScript - Wrap selected text in <quote> tag
"""

# Get the selected text
selected_text = editor.getSelText()

if selected_text:
    # Wrap the selected text with <quote> tags
    wrapped_text = "<quote>" + selected_text + "</quote>"
    
    # Replace the selection with the wrapped text
    editor.replaceSel(wrapped_text)
else:
    # If no text is selected, insert empty tags and position cursor between them
    editor.replaceSel("<quote></quote>")
    # Move cursor back 8 positions (length of "</quote>")
    current_pos = editor.getCurrentPos()
    editor.setCurrentPos(current_pos - 8)
    editor.setSelection(current_pos - 8, current_pos - 8)
