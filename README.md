# Amplitude Project - Extract

This project extracts data from the Amplitude Export API. The tasks for the project included:
- Make a details plan for extracting the data
- Read API documentaiton
- Connect to the API in Python
- Extract the data from the API in Python
- In Python, save the data locally and consider file naming
- Back everything up to GitHub
- Document script

<details>
<summary>Amplitude Export API Documentation</summary>
This API lets you export event data, eg. user interactions on the website. The API documentation specifies the following considerations
<li> Data will include all events up to 2 hrs before API is called </li>
<li> Size limit is 6GB </li>
<li> Calling API required start and end parameters, and to export full day, use T00 and T23 </li>
<li> Max period to query is 365 days </li>
<li> Max 4 concurrent requests and max 360 requests per hour </li>
</details>

From the API documentation, I decided that it needs **Incremental Refreshes**. For my script I decided to set this to daily, so at the start for the script is specifies the start/end parameters for yesterday. The documentation also explains that the output from the API will be a `.zip` file, containing gzip-compressed files of the `.json`. I decided to handle this by creating an additional script for unzipping.

### API output file structure

Outer ZIP File >
  Inner file >
    .gz files for each hour >
        JSON event 
