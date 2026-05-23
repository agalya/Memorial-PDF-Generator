#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memorial PDF Generator - Flask Web Application
Serves HTML form and processes PDF generation requests

Copyright (c) 2026 Agalya

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
import io
from pathlib import Path

# Import the PDF generation logic
from memorial_pdf_generator import generate_memorial_pdf

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main HTML form"""
    return render_template('index.html')


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """Handle PDF generation request"""
    try:
        # Get form data
        title = request.form.get('title', 'Memorial').strip()
        dates = request.form.get('dates', '').strip()
        poem = request.form.get('poem', '').strip()
        author = request.form.get('author', '').strip()
        columns = int(request.form.get('columns', 'auto'))  # 1, 2, or -1 for auto
        
        # Validate required fields
        if not poem:
            return jsonify({'error': 'Poem text is required'}), 400
        
        # Handle photo upload
        photo_data = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                photo_data = file.read()
        
        # Generate PDF
        pdf_bytes = generate_memorial_pdf(
            title=title,
            dates=dates,
            poem=poem,
            author=author,
            photo_data=photo_data,
            num_columns=columns
        )
        
        # Create safe filename from title
        safe_title = secure_filename(title or 'memorial')
        if not safe_title:
            safe_title = 'memorial'
        filename = f"{safe_title}.pdf"
        
        # Return PDF file
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
