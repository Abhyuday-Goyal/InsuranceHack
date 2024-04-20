import PyPDF2
import os


def pdf_to_text(pdf_path):
    # Generate a filename for the text file based on the PDF filename
    pdf_filename = os.path.basename(pdf_path)
    text_filename = os.path.splitext(pdf_filename)[0] + "_extracted.txt"

    # Open the PDF file in binary mode
    with open(pdf_path, "rb") as pdf_file:
        # Create a PDF file reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store text
        text = ""

        # Iterate through each page of the PDF
        for page_num in range(len(pdf_reader.pages)):
            # Get the text from the current page
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # Write the extracted text to a text file
    with open(text_filename, "w", encoding="utf-8") as text_file:
        text_file.write(text)

    return text_filename


# Path to the PDF file you want to convert
pdf_file_path = "boston.pdf"

# Convert PDF to text and get the generated text file name
text_file_path = pdf_to_text(pdf_file_path)

print("Text extracted and saved to", text_file_path)
