# PDF Merger Pro - CLI Guide

Complete guide for using the PDF Merger Pro command-line interface.

## Installation

The CLI is included with PDF Merger Pro. No additional installation needed if you have the project set up.

### Requirements
- Python 3.7+
- Virtual environment activated (or use `.\venv\Scripts\python.exe`)

## Quick Start

```bash
# Show all available commands
python cli.py --help

# Show help for a specific command
python cli.py merge --help

# Check version
python cli.py --version
```

## Commands

### 1. Merge - Combine Multiple PDFs

Merge multiple PDF files into a single document.

**Basic Usage**:
```bash
python cli.py merge file1.pdf file2.pdf file3.pdf -o output.pdf
```

**With Page Selection**:
```bash
# Merge pages 1-5 from file1, all pages from file2, pages 10-15 from file3
python cli.py merge file1.pdf file2.pdf file3.pdf -o output.pdf --pages "1-5,all,10-15"
```

**With Compression**:
```bash
python cli.py merge file1.pdf file2.pdf -o output.pdf --compress
```

**File-Specific Page Ranges**:
```bash
python cli.py merge file1.pdf file2.pdf -o output.pdf --pages "file1.pdf:1-5,file2.pdf:10-20"
```

**Options**:
- `-o, --output` - Output PDF file (required)
- `--pages` - Page ranges for each file
- `--compress` - Compress the output PDF
- `-q, --quiet` - Suppress progress messages

---

### 2. Split - Divide PDF into Multiple Files

Split a PDF file into multiple smaller files.

**Split by Page Count**:
```bash
# Split into files with 10 pages each
python cli.py split input.pdf --pages-per-file 10 -o output_dir/
```

**Split by Page Ranges**:
```bash
# Split into specific page ranges
python cli.py split input.pdf --by-ranges "1-10,11-20,21-30" -o output_dir/
```

**Options**:
- `-o, --output` - Output directory (required)
- `--pages-per-file` - Number of pages per output file
- `--by-ranges` - Split by specific page ranges
- `-q, --quiet` - Suppress progress messages

**Note**: You must specify either `--pages-per-file` or `--by-ranges`.

---

### 3. Extract - Pull Out Specific Pages

Extract specific pages from a PDF file.

**Basic Usage**:
```bash
# Extract pages 1-5 and page 10
python cli.py extract input.pdf --pages "1-5,10" -o extracted.pdf
```

**Extract Single Page**:
```bash
python cli.py extract input.pdf --pages "1" -o page1.pdf
```

**Extract Non-Consecutive Pages**:
```bash
python cli.py extract input.pdf --pages "1,5,10,15-20" -o selected_pages.pdf
```

**Options**:
- `--pages` - Page range to extract (required)
- `-o, --output` - Output PDF file (required)
- `-q, --quiet` - Suppress progress messages

---

### 4. Rotate - Rotate Pages

Rotate pages in a PDF file.

**Rotate All Pages**:
```bash
python cli.py rotate input.pdf --pages "all" --angle 90 -o rotated.pdf
```

**Rotate Specific Pages**:
```bash
# Rotate pages 1-10 by 180 degrees
python cli.py rotate input.pdf --pages "1-10" --angle 180 -o rotated.pdf
```

**Rotate Single Page**:
```bash
python cli.py rotate input.pdf --pages "1" --angle 270 -o rotated.pdf
```

**Options**:
- `--pages` - Page range to rotate (default: "all")
- `--angle` - Rotation angle: 90, 180, or 270 degrees (required)
- `-o, --output` - Output PDF file (required)
- `-q, --quiet` - Suppress progress messages

---

### 5. Watermark - Add Text Watermark

Add a text watermark to all pages of a PDF.

**Basic Usage**:
```bash
python cli.py watermark input.pdf --text "CONFIDENTIAL" -o watermarked.pdf
```

**With Custom Opacity**:
```bash
# Lighter watermark (more transparent)
python cli.py watermark input.pdf --text "DRAFT" --opacity 0.2 -o watermarked.pdf

# Darker watermark (less transparent)
python cli.py watermark input.pdf --text "COPY" --opacity 0.8 -o watermarked.pdf
```

**Options**:
- `--text` - Watermark text (required)
- `--opacity` - Watermark opacity, 0.0 to 1.0 (default: 0.3)
- `-o, --output` - Output PDF file (required)
- `-q, --quiet` - Suppress progress messages

---

### 6. Compress - Reduce File Size

Compress a PDF file to reduce its size.

**Basic Usage**:
```bash
python cli.py compress input.pdf -o compressed.pdf
```

**Quiet Mode**:
```bash
python cli.py compress input.pdf -o compressed.pdf --quiet
```

**Options**:
- `-o, --output` - Output PDF file (required)
- `-q, --quiet` - Suppress progress messages

---

## Batch Processing Examples

### Merge All PDFs in a Directory
```bash
# Windows PowerShell
python cli.py merge (Get-ChildItem *.pdf) -o combined.pdf

# Or specify files explicitly
python cli.py merge file1.pdf file2.pdf file3.pdf -o combined.pdf
```

### Extract First 10 Pages from Multiple Files
```bash
# PowerShell
Get-ChildItem *.pdf | ForEach-Object {
    python cli.py extract $_.FullName --pages "1-10" -o "preview_$($_.Name)"
}
```

### Compress All PDFs in a Directory
```bash
# PowerShell
Get-ChildItem *.pdf | ForEach-Object {
    python cli.py compress $_.FullName -o "compressed_$($_.Name)"
}
```

### Add Watermark to All Files
```bash
# PowerShell
Get-ChildItem *.pdf | ForEach-Object {
    python cli.py watermark $_.FullName --text "CONFIDENTIAL" -o "marked_$($_.Name)"
}
```

### Rotate and Compress Pipeline
```bash
# Rotate first, then compress
python cli.py rotate input.pdf --pages "all" --angle 90 -o rotated.pdf
python cli.py compress rotated.pdf -o final.pdf
```

---

## Advanced Usage

### Page Range Format

Page ranges use a flexible format:
- `all` - All pages
- `5` - Single page (page 5)
- `1-10` - Range of pages (pages 1 through 10)
- `1,5,10` - Specific pages (pages 1, 5, and 10)
- `1-5,10,15-20` - Mixed ranges and specific pages

**Examples**:
```bash
# Extract pages 1-5, page 10, and pages 15-20
python cli.py extract input.pdf --pages "1-5,10,15-20" -o output.pdf

# Merge first 3 pages from file1, all from file2, last 5 pages from file3
python cli.py merge file1.pdf file2.pdf file3.pdf -o output.pdf --pages "1-3,all,96-100"
```

### Quiet Mode

Suppress all progress messages for use in scripts:
```bash
python cli.py merge file1.pdf file2.pdf -o output.pdf --quiet
```

### Exit Codes

The CLI returns standard exit codes:
- `0` - Success
- `1` - Error occurred

Use in scripts:
```bash
python cli.py merge file1.pdf file2.pdf -o output.pdf
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success!"
} else {
    Write-Host "Failed!"
}
```

---

## Scripting Examples

### Automated Report Generation
```powershell
# Merge cover page with report pages
python cli.py merge cover.pdf report.pdf -o final_report.pdf

# Add watermark
python cli.py watermark final_report.pdf --text "DRAFT - $(Get-Date -Format 'yyyy-MM-dd')" -o draft_report.pdf

# Compress for email
python cli.py compress draft_report.pdf -o email_report.pdf
```

### Batch Page Extraction
```powershell
# Extract first page from all PDFs as previews
Get-ChildItem *.pdf | ForEach-Object {
    $outputName = "preview_" + $_.BaseName + ".pdf"
    python cli.py extract $_.FullName --pages "1" -o $outputName
}
```

### Split Large PDF into Chapters
```powershell
# Split a 100-page document into 5 chapters
python cli.py split book.pdf --by-ranges "1-20,21-40,41-60,61-80,81-100" -o chapters/
```

---

## Troubleshooting

### "No module named 'pypdf'"
Make sure you're using the virtual environment:
```bash
.\venv\Scripts\python.exe cli.py --help
```

Or activate the virtual environment first:
```bash
.\venv\Scripts\Activate.ps1
python cli.py --help
```

### "At least 2 PDF files are required for merging"
The merge command requires at least 2 input files:
```bash
# Wrong
python cli.py merge file1.pdf -o output.pdf

# Correct
python cli.py merge file1.pdf file2.pdf -o output.pdf
```

### "Invalid page range format"
Check your page range syntax:
```bash
# Wrong
python cli.py extract input.pdf --pages "1 to 10" -o output.pdf

# Correct
python cli.py extract input.pdf --pages "1-10" -o output.pdf
```

### File Not Found Errors
Use absolute paths or ensure you're in the correct directory:
```bash
# Relative path
python cli.py merge .\pdfs\file1.pdf .\pdfs\file2.pdf -o output.pdf

# Absolute path
python cli.py merge "C:\Documents\file1.pdf" "C:\Documents\file2.pdf" -o output.pdf
```

---

## Tips and Best Practices

1. **Use Quotes for File Paths with Spaces**:
   ```bash
   python cli.py merge "My File 1.pdf" "My File 2.pdf" -o "Output File.pdf"
   ```

2. **Test with Small Files First**:
   Before batch processing, test your command on a small sample.

3. **Use Quiet Mode in Scripts**:
   Add `--quiet` to suppress progress output in automated scripts.

4. **Check Exit Codes**:
   Always check the exit code in scripts to handle errors properly.

5. **Backup Original Files**:
   When modifying PDFs, keep backups of the originals.

6. **Use Compression for Email**:
   Compress PDFs before emailing to reduce file size.

---

## Complete Command Reference

```bash
# General
python cli.py --help                    # Show all commands
python cli.py --version                 # Show version
python cli.py <command> --help          # Show command help

# Merge
python cli.py merge <files...> -o <output> [--pages <ranges>] [--compress] [-q]

# Split
python cli.py split <input> -o <output_dir> [--pages-per-file <n> | --by-ranges <ranges>] [-q]

# Extract
python cli.py extract <input> --pages <range> -o <output> [-q]

# Rotate
python cli.py rotate <input> [--pages <range>] --angle <90|180|270> -o <output> [-q]

# Watermark
python cli.py watermark <input> --text <text> [--opacity <0.0-1.0>] -o <output> [-q]

# Compress
python cli.py compress <input> -o <output> [-q]
```

---

## Support

For issues or questions:
1. Check this guide
2. Use `--help` for command-specific help
3. Verify your Python environment is set up correctly
4. Check that all input files exist and are valid PDFs

---

**PDF Merger Pro CLI v2.0.0**
