"""
A Python script to merge all .txt files in a directory and its subdirectories
into a single output file.

Author: Rodrigo Prestes Machado
"""
import os

class TextMerger:
    """
    A class to merge all .txt files in a directory and its subdirectories
    into a single output file.

    Attributes:
    -----------
    directory : str
        The path to the directory containing the .txt files.
    output_file : str
        The name of the file where the merged content will be saved.
    """

    def __init__(self, directory, output_file):
        """
        Initializes the TextMerger with the directory and output file.

        Parameters:
        -----------
        directory : str
            The path to the directory containing the .txt files.
        output_file : str
            The name of the file where the merged content will be saved.
        """
        self.directory = directory
        self.output_file = output_file

    def merge_files(self):
        """
        Merges all .txt files in the specified directory and subdirectories
        into a single output file.

        This method walks through the directory, reads each .txt file, and
        writes its content to the output file. A newline is added between
        the content of each file.
        """
        with open(self.output_file, 'w', encoding='utf-8') as final_file:
            # Traverse the directory and subdirectories
            for root, dirs, files in os.walk(self.directory):
                for file_name in files:
                    if file_name.endswith('.txt'):
                        file_path = os.path.join(root, file_name)
                        print(f"Reading file: {file_path}")

                        # Read and write the content of the file
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            final_file.write(content)
                            final_file.write('\n\n')

        print(f"Files have been merged into: {self.output_file}")

if __name__ == "__main__":
    # Specify the directory containing the text files and the output file name
    directory = '/Users/rodrigo/Downloads/documentation/'
    output_file = 'merged.txt'

    # Create an instance of the TextMerger class
    merger = TextMerger(directory, output_file)

    # Call the merge_files method to merge the files
    merger.merge_files()
