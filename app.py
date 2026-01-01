# Import Flask class to create a web application
from flask import Flask, render_template, request, send_file

# Import qrcode library to generate QR codes
import qrcode

# Import os module to work with folders and file paths
import os

# Create a Flask app object
# __name__ tells Flask where the app is located
app = Flask(__name__)

# Folder where QR code images will be stored
QR_FOLDER = "static/qr_codes"

# Create the folder if it does not already exist
os.makedirs(QR_FOLDER, exist_ok=True)

# This route runs when the user opens the website (home page)
# methods=["GET", "POST"] allows form submission
@app.route("/", methods=["GET", "POST"])
def index():
    
    # Variable to store QR image path (initially empty)
    qr_path = None

    # Check if user clicked the "Generate QR" button
    if request.method == "POST":
        
        # Get the URL entered by the user from the form
        url = request.form.get("url")
        color = request.form.get("color")
        # Make sure the user entered something
        if url:
            
            # Create a QRCode object
            qr = qrcode.QRCode(
                version=1,      # Controls size of QR code
                box_size=10,    # Size of each QR box
                border=5        # White border around QR
            )

            # Add the URL data to the QR code
            qr.add_data(url)

            # Adjust the QR code size automatically
            qr.make(fit=True)

            # Create QR image with black color and white background
            img = qr.make_image(
                fill_color=color,
                back_color="white"
            )

            # Set path where QR image will be saved
            qr_path = os.path.join(QR_FOLDER, "qrcode.png")

            # Save the QR image as PNG file
            img.save(qr_path)

    # Send the HTML page to browser with QR image (if generated)
    return render_template("index.html", qr_path=qr_path)


# This route runs when user clicks "Download PNG"
@app.route("/download")
def download_qr():
    
    # Send the QR image file to the user for download
    return send_file(
        "static/qr_codes/qrcode.png",
        as_attachment=True
    )


# Run the Flask app
if __name__ == "__main__":
    
    # debug=True automatically reloads app when code changes
    app.run(debug=True)
