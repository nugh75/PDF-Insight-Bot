# PDF Insight Bot: Your QA Interface for PDF Documents

This project is a web interface for question answering (QA) on PDF documents. It uses Streamlit for the user interface, LangChain for handling language and embedding models, and FAISS for indexing and searching.

## Features

- Upload PDF files.
- Select Hugging Face embedding models.
- Select GPT models.
- Input questions and receive answers based on the content of the PDF.
- Save answers to a file.

## Requirements

- Python 3.10.12
- Packages listed in the `requirements.txt` file.
- Ollama configured locally to use GPT models.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/nugh75/PDF-Insight-Bot.git
    cd PDF-Insight-Bot
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuring Ollama Locally

To use Ollama locally with this script, ensure you have Ollama installed and configured. Follow the official Ollama instructions for installation and configuration.

1. Ensure Ollama is running locally and accessible at `http://localhost:11434/v1`.

2. No API key is needed for local Ollama, but make sure the `api_key` parameter is set to "not-needed" in the script.

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```
2. Select the Hugging Face embedding model, the GPT model and temperature.

3. Upload a PDF file via the web interface.

4. Enter your questions (one per line) and click "Get Answers".

5. The answers will be displayed below the questions.

6. To save the answers to a file, enter the file name and click "Save Answers to File". A button will be available to download the file.

### Performance and Speed

The processing of answers and the speed at which responses are generated depend on the performance of the machine you have available. Machines with faster processors and more RAM will generally process answers more quickly. If you are using very complex GPT models or large PDF documents, system performance may significantly impact response time.

## Configuration

### Environment Variables

The `.env` file should contain the following environment variables:

- `API_KEY`: The API key for the ChatOpenAI model (not needed for local Ollama).

### Configuration File

You can configure the embedding models and GPT models by modifying the options in the `app.py` file.

## Example Usage

1. Upload a PDF file via the web interface.
2. Select `sentence-transformers/all-MiniLM-L6-v2` as the embedding model.
3. Select `llama3` as the GPT model.
4. Enter questions in the text field.
5. Click "Get Answers" to see answers based on the content of the PDF.

## Contributing

If you wish to contribute, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the GPLv3 License. See the LICENSE file for more details.


