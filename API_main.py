from flask import Flask, request, send_file
import PyPDF2

app = Flask(__name__)

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    if 'file' not in request.files:
        return "No file part"
    
    uploaded_file = request.files['file']
    
    if uploaded_file.filename == '':
        return "No selected file"
    
    try:
        # Save the uploaded file temporarily
        uploaded_file.save('temp.pdf')

        # Check if the uploaded file is a PDF
        if not uploaded_file.filename.endswith('.pdf'):
            return "Uploaded file is not a PDF"

        # Read the temporary file
        with open('temp.pdf', 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            if pdf_reader.is_encrypted:
                pdf_reader.decrypt('')
                output_path = 'decrypted.pdf'
                with open(output_path, 'wb') as output_file:
                    pdf_writer = PyPDF2.PdfWriter()
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                    pdf_writer.write(output_file)
                return send_file(output_path, as_attachment=True)
            else:
                return "The uploaded PDF is not encrypted"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        # Clean up temporary files
        import os
        os.remove('temp.pdf')
        if os.path.exists('decrypted.pdf'):
            os.remove('decrypted.pdf')

@app.errorhandler(404)
def not_found_error(error):
    return "404 Not Found - The requested URL was not found on the server.", 404

if __name__ == '__main__':
    app.run(debug=True)
