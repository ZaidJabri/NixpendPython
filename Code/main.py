from flask import Flask, render_template, request, make_response, url_for
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/view')
def view():
    # Extract parameters from the URL
    name = request.args.get('name')
    email = request.args.get('email')
    telephone = request.args.get('telephone')

    return render_template('view.html', name=name, email=email, telephone=telephone)


@app.route('/', methods=['POST'])
def getvalue():
    name = request.form['name']
    email = request.form['email']
    telephone = request.form['telephone']

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=2
    )
    # URL to the page that contains the user's inputs
    url = url_for('view', name=name, email=email, telephone=telephone, _external=True, _scheme='http')
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code
    qr_filename = f"qr_{name}.png"
    img.save(qr_filename)

    # Generate PDF
    pdf_filename = f"{name}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    data = []

    # Add QR code to the PDF
    qr_image = Image(qr_filename, width=200, height=200)
    data.append(qr_image)

    # Build the PDF document
    doc.build(data)

    # Serve the PDF as a response to the user
    with open(pdf_filename, "rb") as pdf_file:
        response = make_response(pdf_file.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename={pdf_filename}'

    return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)
