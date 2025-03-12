"""
GitHubMarkdown is a class that handles cloning a GitHub repository, searching
for markdown files in the one directory, and converting them to plain text. The
class provides methods to clone the repository, process the markdown files, and
save the resulting plain text files.

Author: Rodrigo Prestes Machado
"""
import os
import shutil
import markdown2
from bs4 import BeautifulSoup

class GitHubMarkdown:
    """
    GitHubMarkdown handles cloning a GitHub repository, searching for markdown
    files in the one directory, and converting them to plain text.

    Attributes:
        url (str): Base URL of the GitHub repository.
        project_name (str): Name of the project to be cloned.
        repository_url (str): Full URL of the repository.
        output_dir (str): Directory where plain text files are saved.
    """

    def __init__(self, url, project_name, markdown_folder="doc"):
        """
        Initializes the processor with the given URL and project name,
        and automatically clones the repository.

        Args:
            url (str): Base URL of the GitHub repository.
            project_name (str): Name of the project to be cloned.
        """
        self.url = url
        self.project_name = project_name
        self.markdown_folder = markdown_folder
        self.repository_url = os.path.join(url, project_name)
        self.output_dir = "text_files"
        self.clone_repository()

    def clone_repository(self):
        """
        Clones the GitHub repository to the local machine, removing any existing
				folder with the same name.
        """
        self._delete_folder(self.project_name)
        os.system(f"git clone {self.repository_url}")

    def process_markdown_files(self):
        """
        Processes markdown files in the one directory of the project,
        converting them to plain text and saving them in the output
        directory. The original repository folder is deleted after
        processing.
        """
        files = self._get_markdown_files()
        files = [file for file in files if "index.md" not in file]

        self._show_list_files(files)
        self._create_output_directory()

        for file in files:
            self._convert_and_save_markdown(file)

        self._delete_folder(self.project_name)

    def _show_list_files(self, file_array):
        """
        Prints the list of markdown files found.

        Args:
            file_array (list): List of file paths.
        """
        print(file_array)

    def _delete_folder(self, folder):
        """
        Deletes the specified folder if it exists.

        Args:
            folder (str): The folder path to delete.
        """
        if os.path.exists(folder):
            shutil.rmtree(folder)

    def _get_markdown_files(self):
        """
        Retrieves a list of all markdown files in the one directory.

        Returns:
            list: A list of paths to markdown files.
        """
        files = []
        for root, directories, filenames in os.walk(
                os.path.join(self.project_name, self.markdown_folder)):
            for filename in filenames:
                if filename.endswith(".md"):
                    files.append(os.path.join(root, filename))
        return files

    def _create_output_directory(self):
        """
        Creates the output directory if it doesn't already exist.
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _convert_and_save_markdown(self, file):
        """
        Converts a markdown file to plain text, removes specific markdown
				elements, and saves the resulting text to a new file in the output
				directory.

        Args:
            file (str): Path to the markdown file to be converted.
        """
        with open(file, "r", encoding='utf-8') as f:
            content = f.read()

        html = markdown2.markdown(content)
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        # Remove specific markdown elements
        text = text.replace("{: .fs-2 }", "")
        text = text.replace("{: .fs-3 }", "")
        text = text.replace("{: .fs-4 }", "")
        text = text.replace("{: .label .label-red }", "")

        # Remove the first four lines
        text = text.split("\n", 4)[4]

        # Save the cleaned text to a new file
        new_file = os.path.join(self.output_dir,
                                os.path.basename(file).replace(".md", ".txt"))
        with open(new_file, "w", encoding='utf-8') as f:
            f.write(text)

# Example usage
if __name__ == "__main__":

		url = "https://github.com/orion-services"
		project_name = "ai"
		markdown_folder = "doc"

		# Create an instance of the GitHubMarkdown and process the markdown
		# files
		processor = GitHubMarkdown(url, project_name, markdown_folder)
		processor.process_markdown_files()
