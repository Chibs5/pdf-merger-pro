"""
PDF Splitter - Functionality for splitting and extracting pages from PDF files.
"""

from pypdf import PdfWriter, PdfReader
import os
from typing import List, Tuple, Callable, Optional


class PDFSplitterError(Exception):
    """Custom exception for PDF splitter errors."""
    pass


class PDFSplitter:
    """Handles PDF splitting and page extraction operations."""
    
    def __init__(self):
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
    
    def parse_page_range(self, range_str: str, total_pages: int) -> List[int]:
        """
        Parse a page range string into a list of page numbers.
        
        Args:
            range_str: String like "1-5,7,10-12" or "all"
            total_pages: Total number of pages in the PDF
            
        Returns:
            List of page numbers (0-indexed)
            
        Raises:
            PDFSplitterError: If range string is invalid
        """
        if not range_str or range_str.strip().lower() == "all":
            return list(range(total_pages))
        
        pages = []
        parts = range_str.split(',')
        
        try:
            for part in parts:
                part = part.strip()
                if '-' in part:
                    # Range like "1-5"
                    start, end = part.split('-')
                    start = int(start.strip()) - 1  # Convert to 0-indexed
                    end = int(end.strip()) - 1
                    
                    if start < 0 or end >= total_pages or start > end:
                        raise PDFSplitterError(
                            f"Invalid page range: {part}. Pages must be between 1 and {total_pages}"
                        )
                    
                    pages.extend(range(start, end + 1))
                else:
                    # Single page like "7"
                    page = int(part.strip()) - 1  # Convert to 0-indexed
                    
                    if page < 0 or page >= total_pages:
                        raise PDFSplitterError(
                            f"Invalid page number: {int(part)}. Must be between 1 and {total_pages}"
                        )
                    
                    pages.append(page)
            
            # Remove duplicates and sort
            pages = sorted(list(set(pages)))
            return pages
            
        except ValueError as e:
            raise PDFSplitterError(f"Invalid page range format: {range_str}")
    
    def extract_pages(self, input_file: str, page_range: str, output_file: str) -> bool:
        """
        Extract specific pages from a PDF.
        
        Args:
            input_file: Path to input PDF
            page_range: Page range string (e.g., "1-5,7,10-12")
            output_file: Path for output PDF
            
        Returns:
            True if successful
            
        Raises:
            PDFSplitterError: If extraction fails
        """
        if not os.path.exists(input_file):
            raise PDFSplitterError(f"File not found: {input_file}")
        
        try:
            reader = PdfReader(input_file)
            total_pages = len(reader.pages)
            
            # Parse page range
            pages_to_extract = self.parse_page_range(page_range, total_pages)
            
            if not pages_to_extract:
                raise PDFSplitterError("No pages to extract")
            
            self._update_progress(0, len(pages_to_extract), "Extracting pages...")
            
            # Create writer and add pages
            writer = PdfWriter()
            for i, page_num in enumerate(pages_to_extract):
                writer.add_page(reader.pages[page_num])
                self._update_progress(
                    i + 1,
                    len(pages_to_extract),
                    f"Extracted page {page_num + 1}"
                )
            
            # Write output
            with open(output_file, 'wb') as output:
                writer.write(output)
            
            self._update_progress(
                len(pages_to_extract),
                len(pages_to_extract),
                f"Successfully extracted {len(pages_to_extract)} pages"
            )
            
            return True
            
        except Exception as e:
            raise PDFSplitterError(f"Failed to extract pages: {str(e)}")
    
    def split_by_page_count(self, input_file: str, pages_per_file: int, output_dir: str) -> List[str]:
        """
        Split a PDF into multiple files with specified pages per file.
        
        Args:
            input_file: Path to input PDF
            pages_per_file: Number of pages per output file
            output_dir: Directory for output files
            
        Returns:
            List of created file paths
            
        Raises:
            PDFSplitterError: If splitting fails
        """
        if not os.path.exists(input_file):
            raise PDFSplitterError(f"File not found: {input_file}")
        
        if pages_per_file < 1:
            raise PDFSplitterError("Pages per file must be at least 1")
        
        try:
            reader = PdfReader(input_file)
            total_pages = len(reader.pages)
            
            # Create output directory if needed
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Calculate number of output files
            num_files = (total_pages + pages_per_file - 1) // pages_per_file
            
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_files = []
            
            self._update_progress(0, num_files, "Splitting PDF...")
            
            for file_num in range(num_files):
                start_page = file_num * pages_per_file
                end_page = min(start_page + pages_per_file, total_pages)
                
                # Create writer for this file
                writer = PdfWriter()
                for page_num in range(start_page, end_page):
                    writer.add_page(reader.pages[page_num])
                
                # Write output file
                output_file = os.path.join(
                    output_dir,
                    f"{base_name}_part{file_num + 1}.pdf"
                )
                with open(output_file, 'wb') as output:
                    writer.write(output)
                
                output_files.append(output_file)
                
                self._update_progress(
                    file_num + 1,
                    num_files,
                    f"Created {os.path.basename(output_file)}"
                )
            
            self._update_progress(
                num_files,
                num_files,
                f"Successfully split into {num_files} files"
            )
            
            return output_files
            
        except Exception as e:
            raise PDFSplitterError(f"Failed to split PDF: {str(e)}")
    
    def split_by_ranges(self, input_file: str, ranges: List[str], output_dir: str) -> List[str]:
        """
        Split a PDF into multiple files based on page ranges.
        
        Args:
            input_file: Path to input PDF
            ranges: List of page range strings (e.g., ["1-10", "11-20"])
            output_dir: Directory for output files
            
        Returns:
            List of created file paths
            
        Raises:
            PDFSplitterError: If splitting fails
        """
        if not os.path.exists(input_file):
            raise PDFSplitterError(f"File not found: {input_file}")
        
        if not ranges:
            raise PDFSplitterError("No page ranges provided")
        
        try:
            reader = PdfReader(input_file)
            total_pages = len(reader.pages)
            
            # Create output directory if needed
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_files = []
            
            self._update_progress(0, len(ranges), "Splitting PDF by ranges...")
            
            for i, range_str in enumerate(ranges):
                # Parse range
                pages = self.parse_page_range(range_str, total_pages)
                
                if not pages:
                    continue
                
                # Create writer
                writer = PdfWriter()
                for page_num in pages:
                    writer.add_page(reader.pages[page_num])
                
                # Write output file
                output_file = os.path.join(
                    output_dir,
                    f"{base_name}_pages{range_str.replace(',', '_')}.pdf"
                )
                with open(output_file, 'wb') as output:
                    writer.write(output)
                
                output_files.append(output_file)
                
                self._update_progress(
                    i + 1,
                    len(ranges),
                    f"Created file for pages {range_str}"
                )
            
            self._update_progress(
                len(ranges),
                len(ranges),
                f"Successfully created {len(output_files)} files"
            )
            
            return output_files
            
        except Exception as e:
            raise PDFSplitterError(f"Failed to split PDF: {str(e)}")
