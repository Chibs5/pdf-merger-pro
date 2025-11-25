"""
PDF Merger - Core functionality for merging PDF files.
"""

from pypdf import PdfWriter, PdfReader
import os
from typing import List, Callable, Optional, Dict


class PDFMergerError(Exception):
    """Custom exception for PDF merger errors."""
    pass


class PDFMerger:
    """Handles PDF merging operations with progress tracking."""
    
    def __init__(self):
        self.writer = None
        self.progress_callback: Optional[Callable[[int, int, str], None]] = None
    
    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """
        Set a callback function for progress updates.
        
        Args:
            callback: Function that takes (current, total, message) as arguments
        """
        self.progress_callback = callback
    
    def _update_progress(self, current: int, total: int, message: str):
        """Update progress if callback is set."""
        if self.progress_callback:
            self.progress_callback(current, total, message)
    
    def validate_pdf(self, file_path: str) -> bool:
        """
        Validate if a file is a valid PDF.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            PDFMergerError: If file doesn't exist or can't be read
        """
        if not os.path.exists(file_path):
            raise PDFMergerError(f"File not found: {file_path}")
        
        if not file_path.lower().endswith('.pdf'):
            raise PDFMergerError(f"Not a PDF file: {file_path}")
        
        try:
            reader = PdfReader(file_path)
            # Try to access the first page to ensure it's readable
            if len(reader.pages) == 0:
                raise PDFMergerError(f"PDF file is empty: {file_path}")
            return True
        except Exception as e:
            raise PDFMergerError(f"Invalid or corrupted PDF file: {file_path}\nError: {str(e)}")
    
    def parse_page_range(self, range_str: str, total_pages: int) -> List[int]:
        """
        Parse a page range string into a list of page numbers.
        
        Args:
            range_str: String like "1-5,7,10-12" or "all"
            total_pages: Total number of pages in the PDF
            
        Returns:
            List of page numbers (0-indexed)
        """
        if not range_str or range_str.strip().lower() == "all":
            return list(range(total_pages))
        
        pages = []
        parts = range_str.split(',')
        
        try:
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start, end = part.split('-')
                    start = int(start.strip()) - 1
                    end = int(end.strip()) - 1
                    pages.extend(range(start, end + 1))
                else:
                    pages.append(int(part.strip()) - 1)
            
            return sorted(list(set(pages)))
        except ValueError:
            raise PDFMergerError(f"Invalid page range format: {range_str}")
    
    def merge_pdfs(self, input_files: List[str], output_file: str, page_ranges: Optional[Dict[str, str]] = None) -> bool:
        """
        Merge multiple PDF files into a single PDF.
        
        Args:
            input_files: List of paths to PDF files to merge
            output_file: Path where the merged PDF will be saved
            page_ranges: Optional dict mapping file paths to page range strings (e.g., {"file1.pdf": "1-5,10"})
            
        Returns:
            True if successful
            
        Raises:
            PDFMergerError: If merging fails
        """
        if not input_files:
            raise PDFMergerError("No input files provided")
        
        if len(input_files) < 2:
            raise PDFMergerError("At least 2 PDF files are required for merging")
        
        # Validate all input files first
        self._update_progress(0, len(input_files), "Validating PDF files...")
        for i, file_path in enumerate(input_files):
            self.validate_pdf(file_path)
            self._update_progress(i + 1, len(input_files), f"Validated: {os.path.basename(file_path)}")
        
        # Create a new PDF writer
        self.writer = PdfWriter()
        
        # Merge all PDFs
        total_pages = 0
        self._update_progress(0, len(input_files), "Merging PDF files...")
        
        try:
            for i, file_path in enumerate(input_files):
                reader = PdfReader(file_path)
                num_pages = len(reader.pages)
                
                # Get page range for this file
                if page_ranges and file_path in page_ranges:
                    pages_to_add = self.parse_page_range(page_ranges[file_path], num_pages)
                else:
                    pages_to_add = list(range(num_pages))
                
                # Add specified pages from this PDF
                for page_num in pages_to_add:
                    self.writer.add_page(reader.pages[page_num])
                    total_pages += 1
                
                self._update_progress(
                    i + 1, 
                    len(input_files), 
                    f"Added {len(pages_to_add)} pages from {os.path.basename(file_path)}"
                )
            
            # Write the merged PDF to the output file
            self._update_progress(len(input_files), len(input_files), "Writing merged PDF...")
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            with open(output_file, 'wb') as output:
                self.writer.write(output)
            
            self._update_progress(
                len(input_files), 
                len(input_files), 
                f"Successfully merged {len(input_files)} files ({total_pages} pages)"
            )
            
            return True
            
        except Exception as e:
            raise PDFMergerError(f"Failed to merge PDFs: {str(e)}")
    
    def get_pdf_info(self, file_path: str) -> dict:
        """
        Get information about a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary with PDF information (pages, size, etc.)
        """
        try:
            reader = PdfReader(file_path)
            file_size = os.path.getsize(file_path)
            
            return {
                'path': file_path,
                'filename': os.path.basename(file_path),
                'pages': len(reader.pages),
                'size_bytes': file_size,
                'size_mb': round(file_size / (1024 * 1024), 2)
            }
        except Exception as e:
            raise PDFMergerError(f"Failed to read PDF info: {str(e)}")
