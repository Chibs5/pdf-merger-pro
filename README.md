# PDF Merger Pro

A comprehensive PDF manipulation tool with both GUI and CLI interfaces for merging, splitting, rotating, watermarking, and compressing PDF files.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Features

### 🎯 Core Operations
- ✅ **Merge PDFs** - Combine multiple PDF files with page selection
- ✅ **Split PDFs** - Divide PDFs by page count or custom ranges
- ✅ **Extract Pages** - Pull out specific pages from any PDF
- ✅ **Rotate Pages** - Rotate pages by 90°, 180°, or 270°
- ✅ **Add Watermarks** - Apply text watermarks with opacity control
- ✅ **Compress PDFs** - Reduce file size with content compression

### 🖥️ GUI Features
- Professional tabbed interface (Merge, Split, Modify, About)
- Drag-and-drop file support
- Visual file list with reordering
- Real-time progress tracking
- Page range specification for each file
- Standalone Windows executable (no Python needed!)

### ⌨️ CLI Features
- Complete command-line interface for automation
- Batch processing support
- Scriptable operations
- Progress indicators
- Standard exit codes for scripting
- All GUI features available via CLI

## Screenshots

### GUI Interface
The application features a clean, tabbed interface:
- **Merge Tab**: Combine PDFs with page selection
- **Split Tab**: Divide PDFs into multiple files
- **Modify Tab**: Rotate, watermark, and compress

### CLI Interface
```bash
$ python cli.py merge file1.pdf file2.pdf -o output.pdf --pages "1-5,all"
[100%] Successfully merged 2 files
✓ Successfully merged 2 files to: output.pdf
```

## Installation

### For End Users (Windows)

**No installation required!** Just download and run:

1. Download `PDF Merger Pro.exe` from the [releases](../../releases) page
2. Double-click to run
3. Start merging PDFs!

### For Developers

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pdf-merger-pro.git
   cd pdf-merger-pro
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows Command Prompt:
     ```cmd
     venv\Scripts\activate.bat
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Application

#### Option 1: Standalone Executable (Windows)
```bash
# Just double-click PDF Merger Pro.exe
```

#### Option 2: Run with Python
```bash
python main.py
```

### CLI Application

#### Merge PDFs
```bash
# Basic merge
python cli.py merge file1.pdf file2.pdf -o output.pdf

# Merge with page selection
python cli.py merge file1.pdf file2.pdf -o output.pdf --pages "1-5,all"

# Merge and compress
python cli.py merge file1.pdf file2.pdf -o output.pdf --compress
```

#### Split PDFs
```bash
# Split by page count
python cli.py split input.pdf --pages-per-file 10 -o output_dir/

# Split by custom ranges
python cli.py split input.pdf --by-ranges "1-10,11-20,21-30" -o output_dir/
```

#### Extract Pages
```bash
# Extract specific pages
python cli.py extract input.pdf --pages "1-5,10,15-20" -o extracted.pdf
```

#### Rotate Pages
```bash
# Rotate all pages
python cli.py rotate input.pdf --pages "all" --angle 90 -o rotated.pdf

# Rotate specific pages
python cli.py rotate input.pdf --pages "1-10" --angle 180 -o rotated.pdf
```

#### Add Watermark
```bash
# Add watermark with default opacity
python cli.py watermark input.pdf --text "CONFIDENTIAL" -o watermarked.pdf

# Custom opacity
python cli.py watermark input.pdf --text "DRAFT" --opacity 0.5 -o watermarked.pdf
```

#### Compress PDF
```bash
python cli.py compress input.pdf -o compressed.pdf
```

### Batch Processing Examples

#### Compress All PDFs in Directory
```powershell
# PowerShell
Get-ChildItem *.pdf | ForEach-Object {
    python cli.py compress $_.FullName -o "compressed_$($_.Name)"
}
```

#### Add Watermark to Multiple Files
```powershell
# PowerShell
Get-ChildItem *.pdf | ForEach-Object {
    python cli.py watermark $_.FullName --text "CONFIDENTIAL" -o "marked_$($_.Name)"
}
```

#### Extract First Page as Preview
```powershell
# PowerShell
Get-ChildItem *.pdf | ForEach-Object {
    python cli.py extract $_.FullName --pages "1" -o "preview_$($_.Name)"
}
```

## Page Range Format

Page ranges use a flexible, intuitive format:

- `all` - All pages
- `5` - Single page (page 5)
- `1-10` - Range of pages (pages 1 through 10)
- `1,5,10` - Specific pages (pages 1, 5, and 10)
- `1-5,10,15-20` - Mixed ranges and specific pages

**Examples:**
```bash
# Extract pages 1-5, page 10, and pages 15-20
python cli.py extract input.pdf --pages "1-5,10,15-20" -o output.pdf

# Merge first 3 pages from file1, all from file2
python cli.py merge file1.pdf file2.pdf -o output.pdf --pages "1-3,all"
```

## Project Structure

```
PDF Merger/
├── main.py              # GUI application entry point
├── cli.py               # CLI application entry point
├── gui_enhanced.py      # Enhanced tabbed GUI
├── pdf_merger.py        # Core PDF merging logic
├── pdf_splitter.py      # PDF splitting and extraction
├── pdf_modifier.py      # Rotation, watermarking, compression
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── CLI_GUIDE.md        # Comprehensive CLI documentation
├── .gitignore          # Git ignore configuration
└── dist/               # Standalone executables
    └── PDF Merger Pro.exe
```

## Requirements

### For End Users
- Windows 64-bit (for standalone executable)
- No other requirements!

### For Developers
- Python 3.7 or higher
- Dependencies (automatically installed via `requirements.txt`):
  - `pypdf>=4.0.0` - PDF manipulation
  - `tkinterdnd2>=0.3.0` - Drag-and-drop support (optional)
  - `Pillow>=10.0.0` - Image handling
  - `pyinstaller>=6.0.0` - Executable creation (development only)

## Building the Executable

To build the standalone executable yourself:

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Build executable
python -m PyInstaller --name="PDF Merger Pro" --onefile --windowed main.py

# Find the executable in dist/
```

## Documentation

- **[CLI_GUIDE.md](CLI_GUIDE.md)** - Comprehensive CLI documentation with examples
- **[README.md](README.md)** - This file (project overview)
- **Built-in Help** - Use `python cli.py --help` or `python cli.py <command> --help`

## Troubleshooting

### GUI Issues

**Application won't start**
- Make sure you have Python 3.7+ installed: `python --version`
- Try running with: `python main.py`

**Drag-and-drop not working**
- This is normal if `tkinterdnd2` isn't installed
- Use the "Add Files" button instead
- Or install: `pip install tkinterdnd2`

### CLI Issues

**"No module named 'pypdf'"**
```bash
# Make sure you're using the virtual environment
.\venv\Scripts\python.exe cli.py --help

# Or activate it first
.\venv\Scripts\Activate.ps1
python cli.py --help
```

**"At least 2 PDF files are required for merging"**
```bash
# Merge needs at least 2 files
python cli.py merge file1.pdf file2.pdf -o output.pdf
```

**Invalid page range errors**
```bash
# Use correct format: "1-10" not "1 to 10"
python cli.py extract input.pdf --pages "1-10" -o output.pdf
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [pypdf](https://github.com/py-pdf/pypdf) for PDF manipulation
- GUI powered by Python's built-in tkinter
- Drag-and-drop support via [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)

## Changelog

### Version 2.0.0 (Current)
- ✨ Added CLI interface for automation
- ✨ Added page selection for merging
- ✨ Added PDF splitting functionality
- ✨ Added page extraction
- ✨ Added page rotation
- ✨ Added watermarking
- ✨ Added PDF compression
- ✨ Added drag-and-drop support
- 🎨 Redesigned GUI with tabbed interface
- 📚 Comprehensive documentation

### Version 1.0.0
- ✅ Basic PDF merging
- ✅ GUI interface
- ✅ File reordering
- ✅ Progress tracking
- ✅ Standalone executable

## Support

For issues, questions, or suggestions:
- Open an [issue](../../issues)
- Check the [CLI_GUIDE.md](CLI_GUIDE.md) for detailed CLI help
- Review the troubleshooting section above

## Author

Created with ❤️ by [Your Name]

---

**PDF Merger Pro v2.0.0** - Professional PDF manipulation made easy
