# Advanced File to eBook Converter 📚

A modern, user-friendly, and powerful desktop application built with Python and **CustomTkinter**. This tool leverages the industry-leading **Calibre** conversion engine to seamlessly convert PDFs and other documents into fluid eBook formats (EPUB, MOBI, AZW3, etc.) with zero quality loss.

## ✨ Features

* **Modern GUI**: A sleek, dark-themed interface built with CustomTkinter.
* **Batch Processing**: Select and convert hundreds of files at once. A progress bar and status labels keep you updated in real-time.
* **Bilingual Interface**: Live UI translation. Switch between English (EN) and Portuguese (PT) instantly via a dropdown menu.
* **Broad Format Support**: 
  * *Inputs*: `.pdf`, `.epub`, `.mobi`, `.azw3`, `.docx`, `.txt`
  * *Outputs*: `EPUB`, `MOBI`, `AZW3`, `PDF`, `DOCX`, `TXT`
* **Portable & Stealthy**: Uses a local **Calibre Portable** installation as its engine. No installation required on the host machine, and the conversion runs entirely in the background (no flashing command prompts on Windows).
* **Smart Output**: Automatically disables Calibre's generic default covers when converting to EPUB.

## 🚀 Prerequisites

To run this project from the source code, you need:

1. **Python 3.x** installed on your system.
2. **CustomTkinter** library:
   ```bash
   pip install customtkinter
Calibre Portable: The engine that powers the conversions.

🛠️ Setup & Installation
Clone the repository:

Bash
git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
cd your-repo-name
Download Calibre Portable:

Go to the official Calibre Portable download page.

Download and extract the folder.

Rename the extracted folder to exactly Calibre Portable and place it inside the root directory of this project.

Your folder structure should look like this:

Plaintext
📁 your-repo-name
├── 📄 converter_app.py
├── 📄 README.md
└── 📁 Calibre Portable
    ├── 📁 Calibre
    │   ├── 📄 ebook-convert.exe
    │   └── ... (other Calibre files)
Run the Application:

Bash
python converter_app.py
📖 How to Use
Click "Browse" to select one or multiple files (e.g., 500 PDFs).

The output directory will automatically default to the source folder, but you can change it by clicking "Browse" in the Save to section.

Select your desired Output Format from the dropdown menu (e.g., EPUB).

Click "Convert Now". The app will process the files sequentially in the background while updating the progress bar.

⚠️ Notes
PDF to EPUB limitations: Standard text PDFs convert flawlessly. Complex PDFs (multi-column layouts, heavily graphical magazines) may have layout shifts, which is an inherent limitation of converting fixed-layout formats to reflowable formats.

Encoding: The application is built to handle complex characters robustly (UTF-8 encoding handled natively in the background process).

📄 License
This project is open-source.
Note: This application acts as a wrapper/GUI for Calibre, created by Kovid Goyal. Calibre is licensed under the GNU General Public License v3.0.
