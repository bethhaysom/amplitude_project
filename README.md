# Amplitude Data Pipeline Project 
![Phase](https://img.shields.io/badge/Part_1-Extract_Complete-brightgreen) ![Phase 2](https://img.shields.io/badge/Part_2-Load_-lightgrey) ![Phase 3](https://img.shields.io/badge/Part_3-Orchestration_-lightgrey) ![Phase 4](https://img.shields.io/badge/Part_4-Data_Modelling_-lightgrey) ![Phase 5](https://img.shields.io/badge/Part_5-Snowflake_-lightgrey) ![Phase 6](https://img.shields.io/badge/Part_6-dbt_-lightgrey)

## Part 1: Extract

This project extracts daily event data from the Amplitude Export API, stores the compressed archives locally with standardized naming, and unpacks the hourly JSON files for downstream processing.

### Scope & Tasks
- [x] Plan for extracting the data
- [x] Review Amplitude Export API documentation
- [x] Connect to the API and extract data in Python
- [x] Save data locally with standardized file naming
- [x] Build decompression script for nested `.zip` and `.gz` outputs
- [x] Back up scripts to GitHub and document workflow

<details>
<summary>Amplitude Export API Documentation</summary>

> This API lets you export event data, eg. user interactions on the website. The API documentation specifies the following considerations:
> - Data will include all events up to 2 hrs before API is called
> - Size limit is 6GB
> - Calling API requires `start` and `end` parameters, and to export a full day, use `T00` and `T23`
> - Max period to query is 365 days
> - Max 4 concurrent requests and max 360 requests per hour

</details>

From the API documentation, I decided that it needs **Incremental Refreshes**. For my script I decided to set this to daily, so at the start for the script is specifies the start/end parameters for yesterday. The documentation also explains that the output from the API will be a `.zip` file, containing gzip-compressed files of the `.json`. I decided to handle this by creating an additional script for unzipping.

### Script Plan and Breakdown

#### Extract.py
<img width="50%" alt="Extract.py workflow sketch" src="https://github.com/user-attachments/assets/29a2bc9b-e5dc-4af8-9233-2ba93597e476" />

#### Unzip.py
<img width="50%" alt="Unzip.py workflow sketch" src="https://github.com/user-attachments/assets/4c202fcc-4fe6-4569-978e-4f5a899505ef" />


### API output file structure

```text
Outer ZIP File (YYYY-MM-DD.zip)
└── Inner Folder (Project ID)
    └── Hourly .gz files (YYYY-MM-DD_H.json.gz)
        └── Raw JSON event records  <-- End state of Part 1
```

The result from part one is two API scripts which, when run consecutively, output the raw JSON files from the Amplitude Event API
