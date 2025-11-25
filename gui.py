"""
PDF Merger - GUI Application
A user-friendly interface for merging PDF files.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pdf_merger import PDFMerger, PDFMergerError
import threading


class PDFMergerGUI:
    """Main GUI application for PDF merging."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # PDF merger instance
        self.merger = PDFMerger()
        self.merger.set_progress_callback(self.update_progress)
        
        # List to store selected PDF files
        self.pdf_files = []
        
        # Create UI
        self.create_widgets()
        
        # Configure drag and drop
        self.setup_drag_drop()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="PDF Merger", 
            font=('Segoe UI', 20, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Instructions
        instructions = ttk.Label(
            main_frame,
            text="Add PDF files by clicking 'Add Files' button below",
            font=('Segoe UI', 10)
        )
        instructions.grid(row=1, column=0, pady=(0, 10))
        
        # File list frame
        list_frame = ttk.LabelFrame(main_frame, text="PDF Files to Merge", padding="10")
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Listbox with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.file_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED,
            font=('Segoe UI', 10),
            height=10
        )
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.file_listbox.yview)
        
        # Buttons frame
        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(
            button_frame, 
            text="Add Files", 
            command=self.add_files
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Remove Selected", 
            command=self.remove_selected
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Clear All", 
            command=self.clear_all
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Move Up", 
            command=self.move_up
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Move Down", 
            command=self.move_down
        ).pack(side=tk.LEFT, padx=5)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode='determinate',
            length=300
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.progress_label = ttk.Label(
            progress_frame,
            text="Ready to merge PDFs",
            font=('Segoe UI', 9)
        )
        self.progress_label.grid(row=1, column=0)
        
        # Merge button
        self.merge_button = ttk.Button(
            main_frame,
            text="Merge PDFs",
            command=self.merge_pdfs,
            style='Accent.TButton'
        )
        self.merge_button.grid(row=4, column=0, pady=(0, 5))
        
        # Status bar
        self.status_label = ttk.Label(
            main_frame,
            text="No files added",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Segoe UI', 9)
        )
        self.status_label.grid(row=5, column=0, sticky=(tk.W, tk.E))
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality."""
        # Note: tkinterdnd2 needs to be installed separately
        # For now, we'll skip this and rely on the Add Files button
        pass
    
    def add_files(self):
        """Open file dialog to add PDF files."""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if files:
            for file in files:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)
                    filename = os.path.basename(file)
                    self.file_listbox.insert(tk.END, filename)
            
            self.update_status()
    
    def remove_selected(self):
        """Remove selected files from the list."""
        selected = self.file_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select files to remove")
            return
        
        # Remove in reverse order to maintain indices
        for index in reversed(selected):
            self.file_listbox.delete(index)
            del self.pdf_files[index]
        
        self.update_status()
    
    def clear_all(self):
        """Clear all files from the list."""
        if self.pdf_files:
            if messagebox.askyesno("Clear All", "Remove all files from the list?"):
                self.file_listbox.delete(0, tk.END)
                self.pdf_files.clear()
                self.update_status()
    
    def move_up(self):
        """Move selected file up in the list."""
        selected = self.file_listbox.curselection()
        if not selected or selected[0] == 0:
            return
        
        index = selected[0]
        # Swap in list
        self.pdf_files[index], self.pdf_files[index - 1] = \
            self.pdf_files[index - 1], self.pdf_files[index]
        
        # Update listbox
        item = self.file_listbox.get(index)
        self.file_listbox.delete(index)
        self.file_listbox.insert(index - 1, item)
        self.file_listbox.selection_set(index - 1)
    
    def move_down(self):
        """Move selected file down in the list."""
        selected = self.file_listbox.curselection()
        if not selected or selected[0] == len(self.pdf_files) - 1:
            return
        
        index = selected[0]
        # Swap in list
        self.pdf_files[index], self.pdf_files[index + 1] = \
            self.pdf_files[index + 1], self.pdf_files[index]
        
        # Update listbox
        item = self.file_listbox.get(index)
        self.file_listbox.delete(index)
        self.file_listbox.insert(index + 1, item)
        self.file_listbox.selection_set(index + 1)
    
    def update_status(self):
        """Update the status bar."""
        count = len(self.pdf_files)
        if count == 0:
            self.status_label.config(text="No files added")
        elif count == 1:
            self.status_label.config(text="1 file added")
        else:
            self.status_label.config(text=f"{count} files added")
    
    def update_progress(self, current: int, total: int, message: str):
        """Update progress bar and label."""
        if total > 0:
            progress = (current / total) * 100
            self.progress_bar['value'] = progress
        
        self.progress_label.config(text=message)
        self.root.update_idletasks()
    
    def merge_pdfs(self):
        """Merge the selected PDF files."""
        if len(self.pdf_files) < 2:
            messagebox.showwarning(
                "Insufficient Files",
                "Please add at least 2 PDF files to merge"
            )
            return
        
        # Ask for output file
        output_file = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
        
        # Disable merge button during operation
        self.merge_button.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        
        # Run merge in a separate thread to keep UI responsive
        def merge_thread():
            try:
                self.merger.merge_pdfs(self.pdf_files, output_file)
                
                # Show success message
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    f"PDFs merged successfully!\n\nSaved to:\n{output_file}"
                ))
                
                # Reset progress
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Ready to merge PDFs"))
                
            except PDFMergerError as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Merge Failed",
                    f"Failed to merge PDFs:\n\n{str(e)}"
                ))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Merge failed"))
            
            finally:
                # Re-enable merge button
                self.root.after(0, lambda: self.merge_button.config(state=tk.NORMAL))
        
        # Start merge thread
        thread = threading.Thread(target=merge_thread, daemon=True)
        thread.start()


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = PDFMergerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
