PubMed Paper Fetcher
A Python CLI tool to fetch research papers from PubMed, filtering for pharmaceutical and biotech affiliations.

📌 Features
Fetches papers using the PubMed API.
Filters papers with non-academic authors affiliated with pharmaceutical or biotech companies.
Outputs results as a CSV file.
Command-line interface using Typer.
📦 Setup Instructions
1️⃣ Install Poetry
Ensure you have Poetry installed. If not, install it:

bash
Copy
Edit
pip install poetry
Verify the installation:

bash
Copy
Edit
poetry --version
2️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/vinayastar01/pubmed-fetcher.git
cd pubmed-fetcher
3️⃣ Install Dependencies
Run the following command inside the project directory:

bash
Copy
Edit
poetry install
This will set up a virtual environment and install all dependencies.

4️⃣ Activate the Virtual Environment
bash
Copy
Edit
poetry shell
🚀 Usage
Run the CLI Command
Fetch papers using:

bash
Copy
Edit
poetry run get-papers-list "cancer research"
Save results to a CSV file:

bash
Copy
Edit
poetry run get-papers-list "cancer research" --output-file "papers.csv"
🛠 Project Structure
bash
Copy
Edit
Project/
│── main.py        # Functions for fetching paper details
│── poetry.lock                # CLI entry point
│── pyproject.toml         # Poetry configuration
│── README.md              # Documentation
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
bash
Copy
Edit
git checkout -b feature-branch
Make changes and commit:
bash
Copy
Edit
git commit -m "Added new feature"
Push changes:
bash
Copy
Edit
git push origin feature-branch
Create a Pull Request.
📜 License
This project is licensed under the MIT License.

