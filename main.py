"""
PDF Merger Application
Main entry point for the PDF merger GUI application.
"""

import sys
import tkinter as tk
from tkinter import messagebox


def main():
    """Launch the PDF Merger GUI application."""
    try:
        # Import the enhanced GUI module
        from gui_enhanced import PDFMergerGUI, DRAG_DROP_AVAILABLE, TkinterDnD
        import tkinter as tk
        
        # Create the main window with drag-and-drop support if available
        if DRAG_DROP_AVAILABLE:
            root = TkinterDnD.Tk()
        else:
            root = tk.Tk()
        
        # Create the application
        app = PDFMergerGUI(root)
        
        # Start the GUI event loop
        root.mainloop()
        
    except ImportError as e:
        error_msg = f"Failed to import required modules:\n{str(e)}\n\nPlease ensure all dependencies are installed."
        if 'tk' in str(e).lower():
            error_msg += "\n\ntkinter should be included with Python. Try reinstalling Python."
        print(error_msg, file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"An error occurred while starting the application:\n{str(e)}"
        print(error_msg, file=sys.stderr)
        try:
            messagebox.showerror("Application Error", error_msg)
        except:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
