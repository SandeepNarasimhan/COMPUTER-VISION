from fpdf import FPDF
from PIL import Image
import tempfile
import datetime

def generate_pdf_report(pred_class, class_probs, uploaded_image, gradcam_image):
    # Create temporary files for the images
    orig_img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    gradcam_img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name

    uploaded_image.save(orig_img_path)
    gradcam_image.save(gradcam_img_path)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Brain Tumor Classification Report", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    # Prediction result
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, f"Predicted Tumor Type: {pred_class}", ln=True)

    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, "Class Probabilities:", ln=True)

    pdf.cell(200, 8, f"- {pred_class}: {class_probs:.2f}%", ln=True)

    # Original image
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Uploaded MRI Image:", ln=True)
    pdf.image(orig_img_path, x=10, y=pdf.get_y(), w=90)

    # Grad-CAM image
    pdf.set_y(pdf.get_y() + 70)
    pdf.cell(200, 10, "Grad-CAM Visualization:", ln=True)
    pdf.image(gradcam_img_path, x=10, y=pdf.get_y(), w=90)

    # Save PDF
    pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    pdf.output(pdf_path)
    
    return pdf_path