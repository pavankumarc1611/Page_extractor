from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfReader, PdfWriter
import os

# Initialize the app
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    """Extract specific pages from the uploaded PDF."""
    try:
        pdf_file = request.files['pdf_file']
        pages = request.form['pages']
        pages_to_extract = [int(p.strip()) for p in pages.split(",")]

        input_pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        pdf_file.save(input_pdf_path)

        output_pdf_path = os.path.join(UPLOAD_FOLDER, f"extracted_{pdf_file.filename}")
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        for page_number in pages_to_extract:
            writer.add_page(reader.pages[page_number - 1])

        with open(output_pdf_path, 'wb') as output_pdf:
            writer.write(output_pdf)

        return send_file(output_pdf_path, as_attachment=True)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
