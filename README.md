This is the backend for our DEI Visualizer app.  It provides restful endpoints for a database made up of EEO1 data.

I started with 2-dimensional pdfs or pngs from companies.  Using https://www.adobe.com/acrobat/online/pdf-to-excel.html, I converted these to excel files.  I did a bit of manual cleanup on each sheet to get them into a csv form with regularized headers and no extra columns or rows.

Next, I wrote the following program to convert these CSVs to the form that I want and create one long csv to put into the database.
https://github.com/theLP100/eeo1_data_preprocessing -> see the file v2_dataPreprocessing.ipynb.

This program, EEO1-report-backend manages the "get" routes for the database.  (At this time, we don't have "post" or other CRUD routes. I plan to add these once I implement OAuth; at this time, we don't want others to modify the database in any way.)

The routes are as follows:

/query
- Takes in params: company (str), year (int), sortBy ['race', 'gender', or 'job']
- It returns the count of employees in each of the categories for your given sortBy field, filtered by the given company and year, in the following format:
- returns {'labelData': [the names of the labels], 'valueData': [the values matching those labels in the same order]}

/query/company_years_jobs
- This returns a dictionary with keys: company names, and values a dict, containing:
  - 'years': list of valid years, 
  - 'jobs': list of jobs with non-zero employees,
  - 'totalEmployees': dict with keys: years, and values: total employees for that year.
- This endpoint is used by the front end to get the values for the drop-down menus and the total employee count displayed on the page.

/query/get_all
- returns every line of data in the EEO1_data table as dictionaries.
- this was useful for testing and development, but isn't used in the final app.

/adv_query
- This is the main part of the program which enables the advanced mode.
- Takes in params: company, year, sortBy1 (which is a list of job categories), sortBy2 (either 'race' or 'gender').  
  - year will be either an int or a string "all".  if year is "all", job category will only be one job category.
- returns labelData and valueData, lists:
  - labelData is the list of job categories, in the order given in params
  - valueData is a dictionary, with keys: the categories of sortBy2 (eg. ['Male', 'Female']) and values: the count employees in each category. 


There is a test suite with fixtures checking each of these routes.
Note that there is limited error handling (for example, for invalid input) because our front end uses drop-down menus and the /query/company_years_jobs endpoint to ensure that valid input is entered.