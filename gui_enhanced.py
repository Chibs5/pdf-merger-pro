"""
PDF Merger - Enhanced GUI Application
A comprehensive interface for merging, splitting, and modifying PDF files.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
from pdf_merger import PDFMerger, PDFMergerError
from pdf_splitter import PDFSplitter, PDFSplitterError
from pdf_modifier import PDFModifier, PDFModifierError
import threading

# Try to import drag-and-drop support
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    TkinterDnD = tk


class PDFMergerGUI:
    """Main GUI application for PDF operations."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger Pro")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Initialize PDF handlers
        self.merger = PDFMerger()
        self.splitter = PDFSplitter()
        self.modifier = PDFModifier()
        
        # Set progress callbacks
        self.merger.set_progress_callback(self.update_progress)
        self.splitter.set_progress_callback(self.update_progress)
        self.modifier.set_progress_callback(self.update_progress)
        
        # Data storage
        self.merge_files = []  # List of (filepath, page_range) tuples
        self.page_ranges = {}  # Dict mapping filepath to page range string
        
        # Create UI
        self.create_widgets()
        
        # Setup drag and drop if available
        if DRAG_DROP_AVAILABLE:
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
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="PDF Merger Pro",
            font=('Segoe UI', 20, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_merge_tab()
        self.create_split_tab()
        self.create_modify_tab()
        self.create_about_tab()
        
        # Progress frame (shared across all tabs)
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=300
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.progress_label = ttk.Label(
            progress_frame,
            text="Ready",
            font=('Segoe UI', 9)
        )
        self.progress_label.grid(row=1, column=0)
    
    def create_merge_tab(self):
        """Create the Merge tab."""
        merge_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(merge_frame, text="Merge PDFs")
        
        merge_frame.columnconfigure(0, weight=1)
        merge_frame.rowconfigure(1, weight=1)
        
        # Instructions
        instructions = ttk.Label(
            merge_frame,
            text="Add PDF files to merge. You can specify page ranges for each file.",
            font=('Segoe UI', 10)
        )
        instructions.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # File list frame
        list_frame = ttk.LabelFrame(merge_frame, text="Files to Merge", padding="10")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create Treeview for file list with columns
        columns = ('filename', 'pages', 'range')
        self.merge_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        self.merge_tree.heading('filename', text='File Name')
        self.merge_tree.heading('pages', text='Total Pages')
        self.merge_tree.heading('range', text='Page Range')
        
        self.merge_tree.column('filename', width=300)
        self.merge_tree.column('pages', width=100)
        self.merge_tree.column('range', width=150)
        
        self.merge_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.merge_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.merge_tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Add Files", command=self.add_merge_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Set Page Range", command=self.set_page_range).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_merge_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_merge_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Move Up", command=self.move_merge_up).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Move Down", command=self.move_merge_down).pack(side=tk.LEFT, padx=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(merge_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.compress_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame,
            text="Compress output PDF",
            variable=self.compress_var
        ).pack(side=tk.LEFT)
        
        # Merge button
        self.merge_button = ttk.Button(
            merge_frame,
            text="Merge PDFs",
            command=self.merge_pdfs
        )
        self.merge_button.grid(row=3, column=0)
    
    def create_split_tab(self):
        """Create the Split tab."""
        split_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(split_frame, text="Split PDF")
        
        split_frame.columnconfigure(0, weight=1)
        
        # Instructions
        instructions = ttk.Label(
            split_frame,
            text="Split a PDF file into multiple files or extract specific pages.",
            font=('Segoe UI', 10)
        )
        instructions.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Input file selection
        input_frame = ttk.LabelFrame(split_frame, text="Input PDF", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="PDF File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.split_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.split_input_var, state='readonly').grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10)
        )
        ttk.Button(input_frame, text="Browse", command=self.browse_split_input).grid(row=0, column=2)
        
        # Split mode selection
        mode_frame = ttk.LabelFrame(split_frame, text="Split Mode", padding="10")
        mode_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.split_mode_var = tk.StringVar(value="pages")
        
        ttk.Radiobutton(
            mode_frame,
            text="Split by page count",
            variable=self.split_mode_var,
            value="pages"
        ).grid(row=0, column=0, sticky=tk.W)
        
        self.pages_per_file_var = tk.IntVar(value=5)
        ttk.Label(mode_frame, text="Pages per file:").grid(row=0, column=1, padx=(20, 5))
        ttk.Spinbox(
            mode_frame,
            from_=1,
            to=100,
            textvariable=self.pages_per_file_var,
            width=10
        ).grid(row=0, column=2)
        
        ttk.Radiobutton(
            mode_frame,
            text="Extract specific pages",
            variable=self.split_mode_var,
            value="extract"
        ).grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        self.extract_range_var = tk.StringVar(value="1-10")
        ttk.Label(mode_frame, text="Page range:").grid(row=1, column=1, padx=(20, 5), pady=(10, 0))
        ttk.Entry(mode_frame, textvariable=self.extract_range_var, width=15).grid(
            row=1, column=2, pady=(10, 0)
        )
        
        # Output directory
        output_frame = ttk.LabelFrame(split_frame, text="Output", padding="10")
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.split_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.split_output_var, state='readonly').grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10)
        )
        ttk.Button(output_frame, text="Browse", command=self.browse_split_output).grid(row=0, column=2)
        
        # Split button
        self.split_button = ttk.Button(
            split_frame,
            text="Split PDF",
            command=self.split_pdf
        )
        self.split_button.grid(row=4, column=0, pady=(10, 0))
    
    def create_modify_tab(self):
        """Create the Modify tab."""
        modify_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(modify_frame, text="Modify PDF")
        
        modify_frame.columnconfigure(0, weight=1)
        
        # Instructions
        instructions = ttk.Label(
            modify_frame,
            text="Rotate pages, add watermarks, or compress PDF files.",
            font=('Segoe UI', 10)
        )
        instructions.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Input file selection
        input_frame = ttk.LabelFrame(modify_frame, text="Input PDF", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="PDF File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.modify_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.modify_input_var, state='readonly').grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10)
        )
        ttk.Button(input_frame, text="Browse", command=self.browse_modify_input).grid(row=0, column=2)
        
        # Rotation section
        rotate_frame = ttk.LabelFrame(modify_frame, text="Rotate Pages", padding="10")
        rotate_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        rotate_frame.columnconfigure(1, weight=1)
        
        ttk.Label(rotate_frame, text="Page Range:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.rotate_range_var = tk.StringVar(value="all")
        ttk.Entry(rotate_frame, textvariable=self.rotate_range_var).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10)
        )
        
        ttk.Label(rotate_frame, text="Rotation:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.rotation_var = tk.StringVar(value="90")
        rotation_combo = ttk.Combobox(
            rotate_frame,
            textvariable=self.rotation_var,
            values=["90", "180", "270"],
            state='readonly',
            width=10
        )
        rotation_combo.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        ttk.Button(rotate_frame, text="Rotate", command=self.rotate_pages).grid(
            row=1, column=2, padx=(10, 0), pady=(5, 0)
        )
        
        # Watermark section
        watermark_frame = ttk.LabelFrame(modify_frame, text="Add Watermark", padding="10")
        watermark_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        watermark_frame.columnconfigure(1, weight=1)
        
        ttk.Label(watermark_frame, text="Watermark Text:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.watermark_text_var = tk.StringVar(value="CONFIDENTIAL")
        ttk.Entry(watermark_frame, textvariable=self.watermark_text_var).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10)
        )
        
        ttk.Label(watermark_frame, text="Opacity:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.watermark_opacity_var = tk.DoubleVar(value=0.3)
        ttk.Scale(
            watermark_frame,
            from_=0.1,
            to=1.0,
            orient=tk.HORIZONTAL,
            variable=self.watermark_opacity_var
        ).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(watermark_frame, text="Add Watermark", command=self.add_watermark).grid(
            row=1, column=2, padx=(10, 0), pady=(5, 0)
        )
        
        # Compress section
        compress_frame = ttk.LabelFrame(modify_frame, text="Compress PDF", padding="10")
        compress_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(
            compress_frame,
            text="Reduce PDF file size by compressing content streams."
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(compress_frame, text="Compress", command=self.compress_pdf).pack(side=tk.LEFT)
    
    def create_about_tab(self):
        """Create the About tab."""
        about_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(about_frame, text="About")
        
        about_text = """
PDF Merger Pro
Version 2.0

A comprehensive PDF tool for:
• Merging multiple PDFs with page selection
• Splitting PDFs into multiple files
• Extracting specific pages
• Rotating pages
• Adding watermarks
• Compressing PDFs

Features:
✓ Drag-and-drop support (if available)
✓ Page range selection
✓ Progress tracking
✓ Error handling

Created with Python, tkinter, and pypdf
        """
        
        ttk.Label(
            about_frame,
            text=about_text,
            font=('Segoe UI', 10),
            justify=tk.LEFT
        ).pack(pady=20)
        
        if DRAG_DROP_AVAILABLE:
            ttk.Label(
                about_frame,
                text="✓ Drag-and-drop enabled",
                foreground="green"
            ).pack()
        else:
            ttk.Label(
                about_frame,
                text="⚠ Drag-and-drop not available (tkinterdnd2 not installed)",
                foreground="orange"
            ).pack()
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality."""
        if DRAG_DROP_AVAILABLE:
            self.merge_tree.drop_target_register(DND_FILES)
            self.merge_tree.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        """Handle drag and drop files."""
        files = self.root.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith('.pdf'):
                self.add_file_to_merge(file)
    
    # Merge tab methods
    def add_merge_files(self):
        """Add files to merge list."""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        for file in files:
            self.add_file_to_merge(file)
    
    def add_file_to_merge(self, filepath):
        """Add a single file to merge list."""
        if filepath not in [f[0] for f in self.merge_files]:
            try:
                info = self.merger.get_pdf_info(filepath)
                self.merge_files.append((filepath, "all"))
                self.page_ranges[filepath] = "all"
                
                self.merge_tree.insert('', tk.END, values=(
                    info['filename'],
                    info['pages'],
                    "all"
                ))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add file:\n{str(e)}")
    
    def set_page_range(self):
        """Set page range for selected file."""
        selection = self.merge_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file first")
            return
        
        item = selection[0]
        values = self.merge_tree.item(item, 'values')
        filename = values[0]
        
        # Find the file
        filepath = None
        for f, _ in self.merge_files:
            if os.path.basename(f) == filename:
                filepath = f
                break
        
        if not filepath:
            return
        
        # Ask for page range
        current_range = self.page_ranges.get(filepath, "all")
        new_range = simpledialog.askstring(
            "Page Range",
            f"Enter page range for {filename}\n(e.g., '1-5,10,15-20' or 'all'):",
            initialvalue=current_range
        )
        
        if new_range:
            self.page_ranges[filepath] = new_range
            # Update tree
            self.merge_tree.item(item, values=(values[0], values[1], new_range))
    
    def remove_merge_files(self):
        """Remove selected files from merge list."""
        selection = self.merge_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select files to remove")
            return
        
        for item in selection:
            values = self.merge_tree.item(item, 'values')
            filename = values[0]
            
            # Remove from list
            self.merge_files = [(f, r) for f, r in self.merge_files if os.path.basename(f) != filename]
            
            # Remove from tree
            self.merge_tree.delete(item)
    
    def clear_merge_files(self):
        """Clear all files from merge list."""
        if self.merge_files:
            if messagebox.askyesno("Clear All", "Remove all files from the list?"):
                self.merge_files.clear()
                self.page_ranges.clear()
                for item in self.merge_tree.get_children():
                    self.merge_tree.delete(item)
    
    def move_merge_up(self):
        """Move selected file up in the list."""
        selection = self.merge_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        idx = self.merge_tree.index(item)
        if idx > 0:
            self.merge_tree.move(item, '', idx - 1)
            # Also update the internal list
            self.merge_files[idx], self.merge_files[idx - 1] = self.merge_files[idx - 1], self.merge_files[idx]
    
    def move_merge_down(self):
        """Move selected file down in the list."""
        selection = self.merge_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        idx = self.merge_tree.index(item)
        if idx < len(self.merge_files) - 1:
            self.merge_tree.move(item, '', idx + 1)
            # Also update the internal list
            self.merge_files[idx], self.merge_files[idx + 1] = self.merge_files[idx + 1], self.merge_files[idx]
    
    def merge_pdfs(self):
        """Merge the selected PDF files."""
        if len(self.merge_files) < 2:
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
        
        # Disable merge button
        self.merge_button.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        
        # Run merge in a separate thread
        def merge_thread():
            try:
                file_paths = [f for f, _ in self.merge_files]
                self.merger.merge_pdfs(file_paths, output_file, self.page_ranges)
                
                # Compress if requested
                if self.compress_var.get():
                    self.root.after(0, lambda: self.progress_label.config(text="Compressing..."))
                    temp_file = output_file + ".tmp"
                    os.rename(output_file, temp_file)
                    self.modifier.compress_pdf(temp_file, output_file)
                    os.remove(temp_file)
                
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    f"PDFs merged successfully!\n\nSaved to:\n{output_file}"
                ))
                
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Ready"))
                
            except (PDFMergerError, PDFModifierError) as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Merge Failed",
                    f"Failed to merge PDFs:\n\n{str(e)}"
                ))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Failed"))
            
            finally:
                self.root.after(0, lambda: self.merge_button.config(state=tk.NORMAL))
        
        thread = threading.Thread(target=merge_thread, daemon=True)
        thread.start()
    
    # Split tab methods
    def browse_split_input(self):
        """Browse for input PDF to split."""
        file = filedialog.askopenfilename(
            title="Select PDF to split",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file:
            self.split_input_var.set(file)
    
    def browse_split_output(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.split_output_var.set(directory)
    
    def split_pdf(self):
        """Split the PDF file."""
        input_file = self.split_input_var.get()
        output_dir = self.split_output_var.get()
        
        if not input_file:
            messagebox.showwarning("No Input", "Please select a PDF file to split")
            return
        
        if not output_dir:
            messagebox.showwarning("No Output", "Please select an output directory")
            return
        
        self.split_button.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        
        def split_thread():
            try:
                mode = self.split_mode_var.get()
                
                if mode == "pages":
                    pages_per_file = self.pages_per_file_var.get()
                    output_files = self.splitter.split_by_page_count(
                        input_file,
                        pages_per_file,
                        output_dir
                    )
                else:  # extract
                    page_range = self.extract_range_var.get()
                    output_file = os.path.join(
                        output_dir,
                        f"{os.path.splitext(os.path.basename(input_file))[0]}_extracted.pdf"
                    )
                    self.splitter.extract_pages(input_file, page_range, output_file)
                    output_files = [output_file]
                
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    f"PDF split successfully!\n\nCreated {len(output_files)} file(s) in:\n{output_dir}"
                ))
                
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Ready"))
                
            except PDFSplitterError as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Split Failed",
                    f"Failed to split PDF:\n\n{str(e)}"
                ))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Failed"))
            
            finally:
                self.root.after(0, lambda: self.split_button.config(state=tk.NORMAL))
        
        thread = threading.Thread(target=split_thread, daemon=True)
        thread.start()
    
    # Modify tab methods
    def browse_modify_input(self):
        """Browse for input PDF to modify."""
        file = filedialog.askopenfilename(
            title="Select PDF to modify",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file:
            self.modify_input_var.set(file)
    
    def rotate_pages(self):
        """Rotate pages in the PDF."""
        input_file = self.modify_input_var.get()
        
        if not input_file:
            messagebox.showwarning("No Input", "Please select a PDF file")
            return
        
        output_file = filedialog.asksaveasfilename(
            title="Save rotated PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"{os.path.splitext(os.path.basename(input_file))[0]}_rotated.pdf"
        )
        
        if not output_file:
            return
        
        self.progress_bar['value'] = 0
        
        def rotate_thread():
            try:
                page_range = self.rotate_range_var.get()
                rotation = int(self.rotation_var.get())
                
                self.modifier.rotate_pages(input_file, page_range, rotation, output_file)
                
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    f"Pages rotated successfully!\n\nSaved to:\n{output_file}"
                ))
                
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Ready"))
                
            except PDFModifierError as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Rotation Failed",
                    f"Failed to rotate pages:\n\n{str(e)}"
                ))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Failed"))
        
        thread = threading.Thread(target=rotate_thread, daemon=True)
        thread.start()
    
    def add_watermark(self):
        """Add watermark to the PDF."""
        input_file = self.modify_input_var.get()
        
        if not input_file:
            messagebox.showwarning("No Input", "Please select a PDF file")
            return
        
        watermark_text = self.watermark_text_var.get()
        if not watermark_text:
            messagebox.showwarning("No Text", "Please enter watermark text")
            return
        
        output_file = filedialog.asksaveasfilename(
            title="Save watermarked PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"{os.path.splitext(os.path.basename(input_file))[0]}_watermarked.pdf"
        )
        
        if not output_file:
            return
        
        self.progress_bar['value'] = 0
        
        def watermark_thread():
            try:
                opacity = self.watermark_opacity_var.get()
                
                self.modifier.add_text_watermark(
                    input_file,
                    watermark_text,
                    output_file,
                    opacity=opacity
                )
                
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    f"Watermark added successfully!\n\nSaved to:\n{output_file}"
                ))
                
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Ready"))
                
            except PDFModifierError as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Watermark Failed",
                    f"Failed to add watermark:\n\n{str(e)}"
                ))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Failed"))
        
        thread = threading.Thread(target=watermark_thread, daemon=True)
        thread.start()
    
    def compress_pdf(self):
        """Compress the PDF file."""
        input_file = self.modify_input_var.get()
        
        if not input_file:
            messagebox.showwarning("No Input", "Please select a PDF file")
            return
        
        output_file = filedialog.asksaveasfilename(
            title="Save compressed PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"{os.path.splitext(os.path.basename(input_file))[0]}_compressed.pdf"
        )
        
        if not output_file:
            return
        
        self.progress_bar['value'] = 0
        
        def compress_thread():
            try:
                self.modifier.compress_pdf(input_file, output_file)
                
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    f"PDF compressed successfully!\n\nSaved to:\n{output_file}"
                ))
                
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Ready"))
                
            except PDFModifierError as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Compression Failed",
                    f"Failed to compress PDF:\n\n{str(e)}"
                ))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.progress_label.config(text="Failed"))
        
        thread = threading.Thread(target=compress_thread, daemon=True)
        thread.start()
    
    def update_progress(self, current: int, total: int, message: str):
        """Update progress bar and label."""
        if total > 0:
            progress = (current / total) * 100
            self.progress_bar['value'] = progress
        
        self.progress_label.config(text=message)
        self.root.update_idletasks()


def main():
    """Main entry point for the GUI application."""
    if DRAG_DROP_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    
    app = PDFMergerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
