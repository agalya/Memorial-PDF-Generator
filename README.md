# Memorial PDF Generator

A web application to create elegant memorial PDFs with your poem and photos.

## Description

Memorial PDF Generator is a Flask-based web application that allows users to create beautifully formatted PDF memorials with customizable titles, poems, dates, author names, and accompanying images. The application supports both single and multi-column layouts with automatic detection.

## Features

- 📝 **Customizable Titles**: Add a memorable title for your memorial
- 📸 **Photo Support**: Upload and attach photos (JPG, PNG, GIF, WebP)
- ✍️ **Poem Text**: Include meaningful poems or tributes
- 👤 **Author Attribution**: Add author names for credit
- 📄 **Flexible Layouts**: Choose auto-detect, single-column, or two-column layouts
- 🎨 **Beautiful Design**: Elegant dark theme with gold accents
- 📊 **Easy to Use**: Simple, intuitive web interface

## Installation

### Requirements
- Python 3.7+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/memorial-pdf-generator.git
cd memorial-pdf-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
# On Windows
run.bat

# On Linux/Mac
bash run.sh
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Fill in the form fields**:
   - Memorial Title (optional)
   - Upload a Photo (optional)
   - Dates (optional)
   - Poem Text (required)
   - Author Name(s) (optional)
   - Layout preference

2. **Click "Generate PDF"** to create your memorial

3. **Download** the PDF file automatically

## Project Structure

```
memorial-pdf-generator/
├── app.py                          # Flask web application
├── memorial_pdf_generator.py        # Core PDF generation module
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # Web interface
├── run.bat                        # Run script for Windows
├── run.sh                         # Run script for Linux/Mac
└── README.md                      # This file
```

## Dependencies

- Flask 2.3.0+ - Web framework
- fpdf2 2.7.5+ - PDF generation
- Pillow 10.0.0+ - Image processing
- uharfbuzz 0.37.0+ - Font handling

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3). See [LICENSE](LICENSE) file for details.

### License Summary

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).

## Author

**Agalya** - Created this Memorial PDF Generator

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**© 2026 Agalya** | Licensed under GPLv3
