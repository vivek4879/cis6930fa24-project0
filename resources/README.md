
# Functions

The createdb() function is responsible for setting up a SQLite database for storing incident data. Here’s what it does step-by-step:

1. Check if the database already exists:
The function first checks whether a database file named normanpd.db already exists in a folder named resources in the current working directory. If it does, it removes (deletes) this file to ensure a fresh start each time the function is run.
	
 2.	Create the database folder if necessary:
The function uses os.path.join() to construct the path for the resources directory, where the database will be stored. If the folder does not exist, it creates it using os.makedirs().
	
 3.	Set the database file path:
The full path to the normanpd.db file is generated and stored in the db_path variable, which points to the location in the newly created resources folder.
	
 4.	Create a connection to the database:
The sqlite3.connect() function is used to establish a connection to the database. If the database does not exist, this function automatically creates it.
	
 5.	Create a cursor object:
A cursor object (cur) is created to interact with the database. This cursor is used to execute SQL queries.
	
 6.	Drop the existing incidents table:
If a table named incidents exists in the database, it is deleted using the SQL command DROP TABLE IF EXISTS incidents;. This ensures no conflicting data is present.
	
 7.	Create the incidents table:
A new table named incidents is created with the specified columns: incident_time, incident_number, incident_location, nature, and incident_ori. These columns will hold the relevant information about each incident.

 8.	Return the database connection:
The function returns the database connection (con) so that other functions can use it to interact with the database, such as inserting or querying data.


extracting_rows(pdf_path):

This function is responsible for extracting text data from a PDF file located at the path pdf_path. Here’s what the function does:


1. Opening the PDF:
It attempts to open the PDF file in binary mode ("rb") using the PdfReader class from the pypdf library.

2.	Extracting Text from Each Page:
It loops through each page of the PDF and extracts text using page.extract_text(). The method specifies the extraction mode as “layout” and uses additional options (layout_mode_space_vertically = False, layout_mode_scale_weight = 2.0) to control how the text is extracted from the layout of the PDF.

3.	Splitting into Rows:
Once the text for a page is extracted, it is split into rows by breaking the text at newlines (\n). These rows are then added to the all_rows list.

4.	Returning the Rows:
The function removes the first row (return all_rows[1:]), assuming it contains metadata or headings, and returns the rest of the rows as a list.

5.	Handling File Not Found Errors:
If the file is not found (FileNotFoundError), the function returns an empty list.


clean_data(cleaning_list):

This function is responsible for cleaning and structuring the rows of text extracted from the PDF. Here’s how it works:

1.	Skipping Headings or Conclusions:
The function starts by skipping any rows that begin with a certain number of spaces (if(row.startswith("    "))). These rows are likely to be headings or unnecessary data.
2.	Splitting Data by Multiple Spaces:
It uses re.split(r"\s{4,}", row.strip()) to split each row into fields, where fields are separated by four or more spaces. The strip() function is used to remove any leading or trailing spaces.
3.	Building Cleaned Rows:
The function then checks if the number of fields is either 5 (a complete row) or 3 (incomplete row). Based on this:
	•	If the row contains 5 fields, it adds the fields to a new list (cleaned_row_new) and appends it to cleaned_data_to_use.
	•	If the row contains 3 fields, it assumes the remaining fields are missing and fills in empty strings ('') for the missing data.
4.	Returning the Cleaned Data:
The function returns a list of structured data rows (cleaned_data_to_use), where each row has either 5 elements, with missing values properly handled.


fetchincidents(url)

This function is designed to download a PDF file from a given URL and save it locally. It makes use of Python’s built-in urllib library to handle the HTTP request and response. Here’s a breakdown of the key steps:

1.	Setting Headers:
The function defines a dictionary headers to simulate a web browser (using a User-Agent string). This helps in cases where servers block non-browser traffic for security reasons.
2.	Creating a Request:
It creates a request object req using urllib.request.Request with the URL provided and the headers defined. This request is prepared to be sent to the server to download the PDF.
3.	Handling the HTTP Request:
	•	It tries to open the URL using urllib.request.urlopen(req) and reads the content into pdf_data. If successful, the response will contain the binary data of the PDF.
	•	In case of an error (for example, if the URL is unreachable), it catches the urllib.error.URLError and returns None.
4.	Saving the PDF:
	•	If the pdf_data is not empty (i.e., the PDF was successfully downloaded), it writes the PDF data into a file named "incident_report.pdf" in the current directory.
	•	It opens the file in binary write mode ("wb") to ensure that the PDF is correctly saved.
5.	Return Value:
	•	If the PDF is successfully downloaded and saved, the function returns the binary content (pdf_data).
	•	If the download fails, it returns None.

populatedb(con, cleaned_data_to_use)

This function is responsible for populating a SQLite database with incident data that has already been cleaned and structured. The function inserts each record of incident data into the incidents table in the database. Here’s a detailed breakdown:

1.	Cursor Creation:
	•	The function starts by creating a cursor (cur = con.cursor()), which is an object used to interact with the SQLite database. Cursors allow execution of SQL queries and fetching of results.
2.	Insertion Query:
	•	The SQL query insertion_query is a template for inserting data into the incidents table. The placeholders (?) are used to insert values for each column: incident_time, incident_number, incident_location, nature, and incident_ori.
3.	Loop Over Cleaned Data:
	•	The function loops over the cleaned_data_to_use list, which contains rows of data that have been processed earlier (presumably in a format with each incident having five fields).
	•	For each incident (each row in cleaned_data_to_use), it extracts the following fields:
	•	date: the date and time of the incident.
	•	incident_number: the unique incident number.
	•	location: the location where the incident occurred.
	•	nature: the nature or type of the incident (e.g., traffic stop, vandalism).
	•	incident_ori: the originating agency’s identifier.
4.	Data Insertion:
	•	For each row, the extracted values are passed into the SQL query using cur.execute(), which replaces the placeholders (?) with the actual values from the current row.
	•	The database is updated with the new data as the execute function is called.
5.	Error Handling:
	•	If there is an IndexError (typically if a row has fewer than the expected number of fields), the row is skipped, and the error is printed to help with debugging.
	•	If an SQLite-specific error occurs during the insertion (such as a problem with the database connection or query), it rolls back the transaction to prevent partial updates to the database and prints an error message.
6.	Commit Changes:
	•	If all rows are successfully inserted, the function commits the transaction using con.commit(), saving the changes to the database.
7.	Closing the Cursor:
	•	Whether the operation succeeds or fails, the cursor is closed in the finally block, ensuring that resources are properly cleaned up.
