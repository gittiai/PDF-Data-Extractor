# PDF-Data-Extractor

This project extracts **key:value pairs** and **contextual comments** from any PDF and converts them into a **structured Excel file** using an LLM (Groq).

It uses:
- LangChain
- ChatGroq (Groq LLM API)
- PydanticOutputParser
- PDFPlumber
- Streamlit

The system captures 100% of the original text while preserving exact wording.

---

## Features
- Upload any PDF file
- Extract key-value pairs without paraphrasing
- Capture all content with comments/context
- Download a clean Excel file
- Simple Streamlit UI

---

## Project Structure
.
├── main.py
├── requirements.txt
├── README.md

##  Installation  
### 1. Clone the project  
```bash
git clone https://github.com/gittiai/PDF-Data-Extractor.git
cd PDF-Data-Extractor
```
### 2. Create & activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux  
# OR (Windows)  
.venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Add your Groq API Key
```bash
GROQ_API_KEY=your_api_key_here
```
## Usage Instructions

### 1.Run the Streamlit app:
```bash
streamlit run main.py
```
### 2. Open in your browser  
The app will automatically start at:  
**http://localhost:8501**

### 3. Upload a PDF file  
Use the **“Upload PDF”** button to select your document.

### 4. Click “Extract Data”  
The system will then:

- Read your PDF  
- Extract key:value pairs  
- Add contextual comments  
- Generate structured rows  

### 5. Download your Excel file  
Click **“Download Excel File”** to save:

`Output_chatgroq.xlsx`



