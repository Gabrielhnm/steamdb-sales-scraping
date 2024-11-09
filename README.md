# steamdb-sales-scraping
This project is a automation of scraping data from [SteamDB Sales](https://steamdb.info/sales/), export to BigQuery and connect to Google Sheets for analysis

### Features
- **Web Scraping**: Automatically scrapes the latest sales data from SteamDB.
- **Data Storage**: Uploads the scraped data to Google BigQuery to efficient storage, querying, and analysis.
- **Easy Access and Sharing**: Exports the data to a Google Sheets spreadsheet to be easy to view and share.

### Google Sheets
  The data can be viewed [here](https://docs.google.com/spreadsheets/d/1rENYaWXQFyLi_DQuLipdig3HrbjhZvePaSuXeUxs6tk/edit?usp=sharing)

## Requisites
To run this project, ensure you have the following:

1. **Credentials file**:
    You have to create a new service account and download the JSON file to the directory of the repository and rename to `credentials.json`

2. **Share Google Sheets with the Service Account**:
    - Create a new Google Sheets file named `SteamDB Sales` (or open the existing one).
    - Click **Share** and include the service account email as Owner, the service account email can be found in the `client_email` field of the `credentials.json` file.

3. **Link BigQuery to Google Sheets**:
     To connect a BigQuery table to Google Sheets, you can use the Data connectors feature in Google Sheets:
    - Select Data
    - Select Data connectors
    - Select Connect to BigQuery
    - Choose a project
    - Select a table or view
    - Click Connect

### ToDo
- **Scheduling**: Actually the project does not include an automatic scheduling, soon I will try to use Airflow to automate the entire process and have up to date sales.
