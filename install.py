# -*- coding: utf-8 -*-
"""
install.py
Windows installer for Notepad++ PythonScript scripts with keyboard shortcuts.

This script:
1. Detects Notepad++ installation directory
2. Finds PythonScript plugin configuration folder
3. Copies all .py files from local /scripts folder
4. Creates/updates shortcuts.xml with predefined keyboard shortcuts
"""

import os
import sys
import shutil
import winreg
import xml.etree.ElementTree as ET
from pathlib import Path


# Keyboard shortcut mappings
SCRIPT_SHORTCUTS = {
    'wrap_title.py': {'key': '49', 'ctrl': 'yes', 'alt': 'yes', 'shift': 'no'},  # Ctrl+Alt+1
    'wrap_head.py': {'key': '50', 'ctrl': 'yes', 'alt': 'yes', 'shift': 'no'},   # Ctrl+Alt+2
    'wrap_hi.py': {'key': '51', 'ctrl': 'yes', 'alt': 'yes', 'shift': 'no'},     # Ctrl+Alt+3
    'wrap_quote.py': {'key': '52', 'ctrl': 'yes', 'alt': 'yes', 'shift': 'no'},  # Ctrl+Alt+4
    'wrap_trailer.py': {'key': '53', 'ctrl': 'yes', 'alt': 'yes', 'shift': 'no'}, # Ctrl+Alt+5
    'wrap_foreign_prompt.py': {'key': '54', 'ctrl': 'yes', 'alt': 'yes', 'shift': 'no'}, # Ctrl+Alt+6
    'wrap_foreign_fixed.py': {'key': '55', 'ctrl': 'yes', 'alt': 'yes', 'shift': 'no'}, # Ctrl+Alt+7
}


def detect_notepad_install():
    """
    Detect Notepad++ installation directory using Windows Registry.
    
    Returns:
        Path object or None if not found
    """
    registry_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Notepad++"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Notepad++"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Notepad++"),
    ]
    
    for hkey, subkey in registry_paths:
        try:
            key = winreg.OpenKey(hkey, subkey)
            install_dir, _ = winreg.QueryValueEx(key, "")
            winreg.CloseKey(key)
            if install_dir and os.path.isdir(install_dir):
                return Path(install_dir)
        except (WindowsError, FileNotFoundError):
            continue
    
    return None


def get_appdata_notepad_dir():
    """
    Get Notepad++ AppData directory.
    
    Returns:
        Path object to %APPDATA%\\Notepad++\\
    """
    appdata = os.getenv('APPDATA')
    if not appdata:
        raise RuntimeError("APPDATA environment variable not found!")
    
    return Path(appdata) / 'Notepad++'


def get_pythonscript_dir():
    """
    Get PythonScript plugin scripts directory.
    
    Returns:
        Path object to scripts folder
    """
    appdata_npp = get_appdata_notepad_dir()
    return appdata_npp / 'plugins' / 'Config' / 'PythonScript' / 'scripts'


def copy_scripts(source_dir, target_dir):
    """
    Copy all .py files from source to target directory.
    
    Args:
        source_dir: Source directory path
        target_dir: Target directory path
        
    Returns:
        List of copied script names
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    if not source_path.exists():
        raise RuntimeError(f"Source directory not found: {source_path}")
    
    if not target_path.exists():
        raise RuntimeError(
            f"PythonScript scripts directory not found: {target_path}\n\n"
            f"ERROR: This usually means PythonScript plugin is not installed in Notepad++.\n"
            f"Please install PythonScript plugin first:\n"
            f"  1. Open Notepad++\n"
            f"  2. Go to Plugins → Plugins Admin\n"
            f"  3. Find and install 'PythonScript'\n"
            f"  4. Restart Notepad++\n"
            f"  5. Run this installer again"
        )
    
    copied_scripts = []
    py_files = list(source_path.glob('*.py'))
    
    # Filter out test scripts
    py_files = [f for f in py_files if f.name not in ['test_scripts.py']]
    
    if not py_files:
        print("WARNING: No .py files found in scripts directory!")
        return copied_scripts
    
    for py_file in py_files:
        target_file = target_path / py_file.name
        shutil.copy2(py_file, target_file)
        copied_scripts.append(py_file.name)
        print(f"  ✓ Copied: {py_file.name}")
    
    return copied_scripts


def create_or_update_shortcuts(appdata_npp, copied_scripts):
    """
    Create or update shortcuts.xml with keyboard shortcuts for scripts.
    
    Args:
        appdata_npp: Path to Notepad++ AppData directory
        copied_scripts: List of script names that were copied
    """
    shortcuts_file = appdata_npp / 'shortcuts.xml'
    
    # Parse existing file or create new structure
    if shortcuts_file.exists():
        try:
            tree = ET.parse(shortcuts_file)
            root = tree.getroot()
        except ET.ParseError:
            print("WARNING: shortcuts.xml is corrupted, creating new one")
            root = create_empty_shortcuts_xml()
    else:
        root = create_empty_shortcuts_xml()
    
    # Ensure PluginCommands section exists
    plugin_commands = root.find('PluginCommands')
    if plugin_commands is None:
        plugin_commands = ET.SubElement(root, 'PluginCommands')
    
    # Remove existing PythonScript shortcuts for our scripts
    for script_name in SCRIPT_SHORTCUTS.keys():
        script_base = script_name.replace('.py', '')
        command_name = f"PythonScript:{script_base}"
        
        for cmd in plugin_commands.findall('Command'):
            if cmd.get('name') == command_name:
                plugin_commands.remove(cmd)
    
    # Add new shortcuts for copied scripts
    for script_name in copied_scripts:
        if script_name in SCRIPT_SHORTCUTS:
            script_base = script_name.replace('.py', '')
            command_name = f"PythonScript:{script_base}"
            shortcut = SCRIPT_SHORTCUTS[script_name]
            
            cmd_elem = ET.SubElement(plugin_commands, 'Command')
            cmd_elem.set('name', command_name)
            cmd_elem.set('Ctrl', shortcut['ctrl'])
            cmd_elem.set('Alt', shortcut['alt'])
            cmd_elem.set('Shift', shortcut['shift'])
            cmd_elem.set('Key', shortcut['key'])
            
            print(f"  ✓ Shortcut added: {command_name} → Ctrl+Alt+{chr(int(shortcut['key']))}")
    
    # Write XML file with proper formatting
    indent_xml(root)
    tree = ET.ElementTree(root)
    tree.write(shortcuts_file, encoding='utf-8', xml_declaration=True)
    
    print(f"\n✓ Shortcuts saved to: {shortcuts_file}")


def create_empty_shortcuts_xml():
    """
    Create empty shortcuts.xml structure.
    
    Returns:
        ElementTree root element
    """
    root = ET.Element('NotepadPlus')
    ET.SubElement(root, 'InternalCommands')
    ET.SubElement(root, 'Macros')
    ET.SubElement(root, 'UserDefinedCommands')
    ET.SubElement(root, 'PluginCommands')
    ET.SubElement(root, 'ScintillaCommands')
    return root


def indent_xml(elem, level=0):
    """
    Add pretty-printing indentation to XML element.
    
    Args:
        elem: ElementTree element
        level: Current indentation level
    """
    indent = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            indent_xml(child, level + 1)
        # Set tail on last child
        if len(elem) > 0 and (not elem[-1].tail or not elem[-1].tail.strip()):
            elem[-1].tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent


def main():
    """Main installer function."""
    print("=" * 70)
    print("Notepad++ PythonScript Scripts Installer")
    print("=" * 70)
    print()
    
    # Step 1: Detect Notepad++ installation
    print("[1/4] Detecting Notepad++ installation...")
    notepad_dir = detect_notepad_install()
    if notepad_dir:
        print(f"  ✓ Found Notepad++ at: {notepad_dir}")
    else:
        print("  ℹ Notepad++ installation not found in registry (this is OK)")
    print()
    
    # Step 2: Get AppData directory
    print("[2/4] Locating PythonScript configuration...")
    try:
        appdata_npp = get_appdata_notepad_dir()
        pythonscript_dir = get_pythonscript_dir()
        print(f"  ✓ AppData directory: {appdata_npp}")
        print(f"  ✓ PythonScript scripts: {pythonscript_dir}")
    except RuntimeError as e:
        print(f"  ✗ ERROR: {e}")
        return 1
    print()
    
    # Step 3: Copy scripts
    print("[3/4] Copying script files...")
    try:
        script_source = Path(__file__).parent / 'scripts'
        copied_scripts = copy_scripts(script_source, pythonscript_dir)
        print(f"\n  Total scripts copied: {len(copied_scripts)}")
    except RuntimeError as e:
        print(f"  ✗ ERROR: {e}")
        return 1
    print()
    
    # Step 4: Update shortcuts
    print("[4/4] Configuring keyboard shortcuts...")
    try:
        create_or_update_shortcuts(appdata_npp, copied_scripts)
    except Exception as e:
        print(f"  ✗ ERROR: Failed to update shortcuts: {e}")
        return 1
    print()
    
    # Success message
    print("=" * 70)
    print("✓ Installation completed successfully!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Restart Notepad++ to activate the keyboard shortcuts")
    print("  2. Scripts are now available in: Plugins → PythonScript → Scripts")
    print("  3. Use the following keyboard shortcuts:")
    print()
    for script_name, shortcut in SCRIPT_SHORTCUTS.items():
        if script_name in copied_scripts:
            key_char = chr(int(shortcut['key']))
            script_base = script_name.replace('.py', '')
            print(f"     • {script_base:20s} → Ctrl+Alt+{key_char}")
    print()
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
