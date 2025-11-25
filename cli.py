"""
PDF Merger Pro - Command Line Interface
A powerful CLI for PDF operations including merge, split, rotate, watermark, and compress.
"""

import argparse
import sys
import os
from pdf_merger import PDFMerger, PDFMergerError
from pdf_splitter import PDFSplitter, PDFSplitterError
from pdf_modifier import PDFModifier, PDFModifierError


VERSION = "2.0.0"


class ProgressPrinter:
    """Simple progress printer for CLI."""
    
    def __init__(self, quiet=False):
        self.quiet = quiet
        self.last_message = ""
    
    def __call__(self, current, total, message):
        """Print progress updates."""
        if self.quiet:
            return
        
        if total > 0:
            percent = (current / total) * 100
            # Clear previous line and print new progress
            print(f"\r[{percent:3.0f}%] {message}", end='', flush=True)
        else:
            print(f"\r{message}", end='', flush=True)
        
        self.last_message = message
        
        # Print newline when complete
        if current == total and total > 0:
            print()


def merge_command(args):
    """Execute merge command."""
    try:
        merger = PDFMerger()
        progress = ProgressPrinter(args.quiet)
        merger.set_progress_callback(progress)
        
        # Parse page ranges if provided
        page_ranges = {}
        if args.pages:
            # Format: "file1.pdf:1-5,file2.pdf:all"
            # Or simple: "1-5,all,10-15" for all files in order
            if ':' in args.pages:
                # File-specific ranges
                for spec in args.pages.split(','):
                    if ':' in spec:
                        filename, range_str = spec.split(':', 1)
                        # Find matching file
                        for filepath in args.files:
                            if os.path.basename(filepath) == filename or filepath == filename:
                                page_ranges[filepath] = range_str
                                break
            else:
                # Simple comma-separated ranges for files in order
                ranges = args.pages.split(',')
                for i, filepath in enumerate(args.files):
                    if i < len(ranges):
                        page_ranges[filepath] = ranges[i].strip()
                    else:
                        page_ranges[filepath] = "all"
        
        # Merge PDFs
        merger.merge_pdfs(args.files, args.output, page_ranges if page_ranges else None)
        
        # Compress if requested
        if args.compress:
            if not args.quiet:
                print("Compressing output...")
            modifier = PDFModifier()
            modifier.set_progress_callback(progress)
            temp_file = args.output + ".tmp"
            os.rename(args.output, temp_file)
            modifier.compress_pdf(temp_file, args.output)
            os.remove(temp_file)
        
        print(f"✓ Successfully merged {len(args.files)} files to: {args.output}")
        return 0
        
    except PDFMergerError as e:
        print(f"✗ Merge failed: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}", file=sys.stderr)
        return 1


def split_command(args):
    """Execute split command."""
    try:
        splitter = PDFSplitter()
        progress = ProgressPrinter(args.quiet)
        splitter.set_progress_callback(progress)
        
        if args.pages_per_file:
            # Split by page count
            output_files = splitter.split_by_page_count(
                args.input,
                args.pages_per_file,
                args.output
            )
            print(f"✓ Successfully split into {len(output_files)} files in: {args.output}")
        elif args.by_ranges:
            # Split by ranges
            ranges = [r.strip() for r in args.by_ranges.split(',')]
            output_files = splitter.split_by_ranges(
                args.input,
                ranges,
                args.output
            )
            print(f"✓ Successfully split into {len(output_files)} files in: {args.output}")
        else:
            print("✗ Error: Must specify either --pages-per-file or --by-ranges", file=sys.stderr)
            return 1
        
        return 0
        
    except PDFSplitterError as e:
        print(f"✗ Split failed: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}", file=sys.stderr)
        return 1


def extract_command(args):
    """Execute extract command."""
    try:
        splitter = PDFSplitter()
        progress = ProgressPrinter(args.quiet)
        splitter.set_progress_callback(progress)
        
        splitter.extract_pages(args.input, args.pages, args.output)
        
        print(f"✓ Successfully extracted pages to: {args.output}")
        return 0
        
    except PDFSplitterError as e:
        print(f"✗ Extract failed: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}", file=sys.stderr)
        return 1


def rotate_command(args):
    """Execute rotate command."""
    try:
        modifier = PDFModifier()
        progress = ProgressPrinter(args.quiet)
        modifier.set_progress_callback(progress)
        
        modifier.rotate_pages(args.input, args.pages, args.angle, args.output)
        
        print(f"✓ Successfully rotated pages to: {args.output}")
        return 0
        
    except PDFModifierError as e:
        print(f"✗ Rotate failed: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}", file=sys.stderr)
        return 1


def watermark_command(args):
    """Execute watermark command."""
    try:
        modifier = PDFModifier()
        progress = ProgressPrinter(args.quiet)
        modifier.set_progress_callback(progress)
        
        modifier.add_text_watermark(
            args.input,
            args.text,
            args.output,
            opacity=args.opacity
        )
        
        print(f"✓ Successfully added watermark to: {args.output}")
        return 0
        
    except PDFModifierError as e:
        print(f"✗ Watermark failed: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}", file=sys.stderr)
        return 1


def compress_command(args):
    """Execute compress command."""
    try:
        modifier = PDFModifier()
        progress = ProgressPrinter(args.quiet)
        modifier.set_progress_callback(progress)
        
        modifier.compress_pdf(args.input, args.output)
        
        print(f"✓ Successfully compressed to: {args.output}")
        return 0
        
    except PDFModifierError as e:
        print(f"✗ Compress failed: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}", file=sys.stderr)
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='pdf-cli',
        description='PDF Merger Pro - Command Line Interface',
        epilog='For detailed help on a command, use: pdf-cli <command> --help'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'PDF Merger Pro CLI v{VERSION}'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress progress messages'
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Merge command
    merge_parser = subparsers.add_parser(
        'merge',
        help='Merge multiple PDF files',
        description='Merge multiple PDF files into a single PDF with optional page selection'
    )
    merge_parser.add_argument(
        'files',
        nargs='+',
        help='PDF files to merge'
    )
    merge_parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output PDF file'
    )
    merge_parser.add_argument(
        '--pages',
        help='Page ranges for each file (e.g., "1-5,all,10-15" or "file1.pdf:1-5,file2.pdf:all")'
    )
    merge_parser.add_argument(
        '--compress',
        action='store_true',
        help='Compress the output PDF'
    )
    
    # Split command
    split_parser = subparsers.add_parser(
        'split',
        help='Split a PDF into multiple files',
        description='Split a PDF file by page count or page ranges'
    )
    split_parser.add_argument(
        'input',
        help='Input PDF file'
    )
    split_parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output directory'
    )
    split_parser.add_argument(
        '--pages-per-file',
        type=int,
        help='Number of pages per output file'
    )
    split_parser.add_argument(
        '--by-ranges',
        help='Split by page ranges (e.g., "1-10,11-20,21-30")'
    )
    
    # Extract command
    extract_parser = subparsers.add_parser(
        'extract',
        help='Extract specific pages from a PDF',
        description='Extract specific pages from a PDF file'
    )
    extract_parser.add_argument(
        'input',
        help='Input PDF file'
    )
    extract_parser.add_argument(
        '--pages',
        required=True,
        help='Page range to extract (e.g., "1-5,10,15-20")'
    )
    extract_parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output PDF file'
    )
    
    # Rotate command
    rotate_parser = subparsers.add_parser(
        'rotate',
        help='Rotate pages in a PDF',
        description='Rotate specific pages in a PDF file'
    )
    rotate_parser.add_argument(
        'input',
        help='Input PDF file'
    )
    rotate_parser.add_argument(
        '--pages',
        default='all',
        help='Page range to rotate (e.g., "1-10" or "all")'
    )
    rotate_parser.add_argument(
        '--angle',
        type=int,
        choices=[90, 180, 270],
        required=True,
        help='Rotation angle (90, 180, or 270 degrees)'
    )
    rotate_parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output PDF file'
    )
    
    # Watermark command
    watermark_parser = subparsers.add_parser(
        'watermark',
        help='Add a watermark to a PDF',
        description='Add a text watermark to all pages of a PDF'
    )
    watermark_parser.add_argument(
        'input',
        help='Input PDF file'
    )
    watermark_parser.add_argument(
        '--text',
        required=True,
        help='Watermark text'
    )
    watermark_parser.add_argument(
        '--opacity',
        type=float,
        default=0.3,
        help='Watermark opacity (0.0 to 1.0, default: 0.3)'
    )
    watermark_parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output PDF file'
    )
    
    # Compress command
    compress_parser = subparsers.add_parser(
        'compress',
        help='Compress a PDF file',
        description='Reduce PDF file size by compressing content streams'
    )
    compress_parser.add_argument(
        'input',
        help='Input PDF file'
    )
    compress_parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output PDF file'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Show help if no command specified
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == 'merge':
        return merge_command(args)
    elif args.command == 'split':
        return split_command(args)
    elif args.command == 'extract':
        return extract_command(args)
    elif args.command == 'rotate':
        return rotate_command(args)
    elif args.command == 'watermark':
        return watermark_command(args)
    elif args.command == 'compress':
        return compress_command(args)
    else:
        print(f"✗ Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
