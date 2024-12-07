
# cis6930fa24 -- Project 0 -- Incident Report Processing

## Name: Vivek Milind Aher

---

## Project Description

This project processes incident report PDFs from the Norman, Oklahoma Police Department, extracting and storing data in an SQLite database for analysis. The program performs the following tasks:
- Downloads incident reports as PDFs from a provided URL.
- Extracts relevant fields: `Date / Time`, `Incident Number`, `Location`, `Nature`, and `Incident ORI`.
- Creates and populates an SQLite database to store the extracted data.
- Outputs a summary of the `Nature` of incidents and their frequency.

---

## How to Install
1. Install the required dependencies using `pipenv`:
   ```bash
   pipenv install
   ```
2. Ensure the necessary Python libraries are installed, including `pypdf`, `sqlite3`, and `argparse`.

---

## How to Run
To execute the project:
1. Run the following command, replacing `<url>` with the URL of the PDF:
   ```bash
   pipenv run python project0/main.py --incidents <url>
   ```
2. Example:
   ```bash
   pipenv run python project0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf
   ```

---

## Functions
### ** main.py**
- **`main(url)`**  
  - **Parameters:**  
    - `url` (str): URL of the PDF file to download and process.
  - **Process:**  
    - Downloads the PDF file using `fetchincidents`.
    - Extracts raw data from the PDF using `extracting_rows`.
    - Cleans and structures the extracted data using `clean_data`.
    - Creates the SQLite database using `createdb`.
    - Populates the database with cleaned data using `populatedb`.
    - Calls `status` to print the summary of incidents.
  - **Returns:**  
    - None (prints the incident summary).

- **`status(con)`**  
  - **Parameters:**  
    - `con` (sqlite3.Connection): SQLite database connection object.
  - **Process:**  
    - Queries the database to count the frequency of each `Nature` of incidents.
    - Prints the counts sorted alphabetically and case-sensitively.
  - **Returns:**  
    - None (prints the counts in the format `Nature|Count`).

---

### **fetchingincidents.py**
- **`fetchincidents(url)`**  
  - **Parameters:**  
    - `url` (str): URL of the PDF file to download.
  - **Process:**  
    - Sends an HTTP request to download the PDF file.
    - Writes the downloaded data to a file named `incident_report.pdf`.
  - **Returns:**  
    - The raw PDF data as bytes if successful.
    - `None` if the download fails.

---

### **extractingincidents.py**
- **`extracting_rows(pdf_path)`**  
  - **Parameters:**  
    - `pdf_path` (str): Path to the PDF file to process.
  - **Process:**  
    - Reads the PDF file using the `PdfReader` from `pypdf`.
    - Extracts text from each page and splits it into rows.
    - Returns all rows except the header row.
  - **Returns:**  
    - A list of strings where each string represents a row of extracted text.

- **`clean_data(cleaning_list)`**  
  - **Parameters:**  
    - `cleaning_list` (list of str): Raw rows of text extracted from the PDF.
  - **Process:**  
    - Strips unnecessary spaces and splits rows into columns using regular expressions.
    - Handles edge cases (e.g., rows with missing columns).
    - Ensures each row has five fields: `Date / Time`, `Incident Number`, `Location`, `Nature`, `Incident ORI`.
  - **Returns:**  
    - A list of cleaned rows, each represented as a list of five strings.

---

### **creating_database.py**
- **`createdb()`**  
  - **Parameters:**  
    - None.
  - **Process:**  
    - Creates an SQLite database file `normanpd.db` in the `resources` directory.
    - Defines the `incidents` table schema with five columns:
      - `incident_time`: TEXT
      - `incident_number`: TEXT
      - `incident_location`: TEXT
      - `nature`: TEXT
      - `incident_ori`: TEXT
    - Drops the table if it already exists to ensure a fresh start.
  - **Returns:**  
    - An SQLite database connection object.

---

### **populatedb.py**
- **`populatedb(con, cleaned_data_to_use)`**  
  - **Parameters:**  
    - `con` (sqlite3.Connection): SQLite database connection object.
    - `cleaned_data_to_use` (list of lists): Cleaned data ready for insertion.
  - **Process:**  
    - Iterates through the cleaned data and inserts each row into the `incidents` table.
    - Handles errors (e.g., rows with missing fields) by skipping problematic rows.
    - Commits the transaction after all rows are processed.
  - **Returns:**  
    - None (inserts data into the database).

---

## Database Development

The SQLite database (`normanpd.db`) is created in the `resources/` directory with the following schema:
```sql
CREATE TABLE incidents (
    incident_time TEXT,
    incident_number TEXT,
    incident_location TEXT,
    nature TEXT,
    incident_ori TEXT
);
```
- The database ensures each incident is properly stored and retrievable for analysis.
- Any duplicate or erroneous data is handled by skipping problematic rows.

---

## Bugs and Assumptions
- **Assumptions:**
  - Incident reports follow a consistent format.
  - PDF structure allows extraction without errors.
- **Known Issues:**
  - PDFs with unexpected layouts may cause extraction errors.
  - Edge cases with missing or incomplete data are skipped.

---

## How to Test
1. Use `pytest` to run tests:
   ```bash
   pipenv run python -m pytest
   ```
2. Test files include:
   - `test_download.py`: Verifies the `fetchincidents` function.
   - `test_random.py`: Covers extraction, database creation, and data population.

---

## Collaborators and Acknowledgments
Refer to `COLLABORATORS.md` for detailed information on collaboration.  
Special thanks to the Norman Police Department for making data publicly available.


