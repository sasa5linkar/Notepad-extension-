# -*- coding: utf-8 -*-
"""
Notepad++ PythonScript - Wrap selected text in <foreign> tag
"""

# Get the selected text
selected_text = editor.getSelText()

if selected_text:
    # Wrap the selected text with <foreign> tags
    wrapped_text = "<foreign>" + selected_text + "</foreign>"
    
    # Replace the selection with the wrapped text
    editor.replaceSel(wrapped_text)
else:
    # If no text is selected, insert empty tags and position cursor between them
    editor.replaceSel("<foreign></foreign>")
    # Move cursor back 10 positions (length of "</foreign>")
    current_pos = editor.getCurrentPos()
    editor.setCurrentPos(current_pos - 10)
    editor.setSelection(current_pos - 10, current_pos - 10)
