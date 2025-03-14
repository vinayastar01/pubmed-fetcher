# PubMed Paper Fetcher

A Python CLI tool to fetch research papers from PubMed, filtering for pharmaceutical and biotech affiliations.

## Features

- Fetches papers using the PubMed API.
- Filters papers with non-academic authors affiliated with pharmaceutical or biotech companies.
- Outputs results as a CSV file.
- Command-line interface using Typer.

## Setup Instructions

### 1️⃣ Install Poetry
Ensure you have Poetry installed. If not, install it:

```bash
pip install poetry
Verify the installation:


poetry --version

2️⃣ Clone the Repository
Clone the repository to your local machine:


git clone https://github.com/vinayastar01/pubmed-fetcher.git
cd pubmed-fetcher

3️⃣ Install Dependencies
Run the following command inside the project directory:

poetry install
This will set up a virtual environment and install all dependencies.

4️⃣ Activate the Virtual Environment
Activate the virtual environment:

bash
Copy
Edit
poetry shell

🚀 Usage

Fetch papers using:

poetry run python main.py "cancer research"
Save results to a CSV file:

poetry run poetry "cancer research" --output-file "papers.csv"
🛠 Project Structure
bash
Copy
Edit
Project/
│── main.py               # Functions for fetching paper details
│── poetry.lock           # Poetry lock file
│── pyproject.toml        # Poetry configuration
│── README.md             # Documentation
📝 Dependencies

requests – To interact with the PubMed API.
biopython – For parsing PubMed data.
pandas – For processing and saving data.
typer – To create a command-line interface.
rich – For colored terminal output.
All dependencies are managed using Poetry.

🛠 Development
To contribute:

Fork the repository.

Create a new branch:


git checkout -b feature-branch
Make changes and commit:


git commit -m "Added new feature"
Push changes:


git push origin feature-branch
Create a Pull Request.

📜 License

This project is licensed under the MIT License.



Feel free to modify this as per your requirements!


