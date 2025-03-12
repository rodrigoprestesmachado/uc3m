import PyPDF2
import textwrap

class OrionPdf2Text:
    """
    A class to convert PDF files to text and save the text to a file with word
    wrapping.

    Attributes:
        pdf_path (str): The path to the PDF file to be converted.

    Methods:
        convert_to_text():
            Converts the PDF file to text.
            Returns:
                str: The extracted text from the PDF file.
                None: If an error occurs during the conversion process.

        save_text_to_file(output_path, text, width=80):
            Saves the provided text to a .txt file with word wrapping.
            Parameters:
                output_path (str): The path where the text file will be saved.
                text (str): The text to be saved.
                width (int, optional): The maximum line width for word wrapping.
                Default is 80.
    """

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    # Method to convert a PDF file to text
    def convert_to_text(self):
        """
        Converts the content of a PDF file to text.

        This method opens a PDF file specified by the `pdf_path` attribute,
        reads its content, and extracts text from each page. The extracted text
        from all pages is concatenated into a single string with each page's
        text separated by a newline character.

        Returns:
            str: The full text extracted from the PDF file, or None if an error
            occurs.

        Raises:
            Exception: If an error occurs while reading the PDF file, an error
            message is printed and None is returned.
        """
        try:
            # Open the PDF file in binary mode
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                full_text = ""

                # Iterate through all pages and extract text
                for page in range(len(reader.pages)):
                    current_page = reader.pages[page]
                    full_text += current_page.extract_text() + "\n"

                return full_text
        except Exception as e:
            # Print an error message if something goes wrong
            print(f"An error occurred while reading the PDF: {e}")
            return None

    # Method to save text to a .txt file with word wrapping
    def save_text_to_file(self, output_path, text, width=80):
        """
        Saves the provided text to a file, wrapping lines to the specified width.

        Args:
            output_path (str): The path where the text file will be saved.
            text (str): The text content to be saved in the file.
            width (int, optional): The maximum line width for wrapping the text.
            Defaults to 80.

        Returns:
            None
        """
        wrapped_text = "\n".join(textwrap.wrap(text, width=width))
        with open(output_path, "w") as text_file:
            text_file.write(wrapped_text)

if __name__ == "__main__":
    PATH = "manuscript.pdf"
    converter = OrionPdf2Text(PATH)
    text = converter.convert_to_text()
    if text:
        # Save the wrapped text to a new .txt file
        converter.save_text_to_file("output.txt", text)
