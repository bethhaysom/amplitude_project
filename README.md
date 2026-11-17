# Amplitude Data Pipeline Project 
![Phase](https://img.shields.io/badge/Part_1-Extract_Complete-brightgreen) ![Phase 2](https://img.shields.io/badge/Part_2-Load_-brightgreen) ![Phase 3](https://img.shields.io/badge/Part_3-Orchestration_-lightgrey) ![Phase 4](https://img.shields.io/badge/Part_4-Data_Modelling_-lightgrey) ![Phase 5](https://img.shields.io/badge/Part_5-Snowflake_-lightgrey) ![Phase 6](https://img.shields.io/badge/Part_6-dbt_-lightgrey)

## Part 1: Extract

Extracting daily event data from the Amplitude Export API, stores the compressed archives locally with standardized naming, and unpacks the hourly JSON files for downstream processing.

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

#### Python Script Sketches
<img width="90%" alt="Python workflow sketch" src="https://github.com/user-attachments/assets/8c08c86f-15e6-417d-91bc-d618d5be0340" />


#### API output file structure

```text
Outer ZIP File (YYYY-MM-DD.zip)
└── Inner Folder (Project ID)
    └── Hourly .gz files (YYYY-MM-DD_H.json.gz)
        └── Raw JSON event records  <-- End state of Part 1
```

The result from part one is two API scripts which, when run consecutively, output the raw JSON files from the Amplitude Event API


## Part 2: Load (S3 & Snowflake)

The extracted `.json` files are loaded into an S3 bucket, before being loaded into Snowflake.

### Scope & Tasks
- [x] Create an AWS S3 bucket for staging extracted Amplitude JSON data
- [x] Configure an AWS KMS key for server-side encryption
- [x] Set up IAM users, roles, and least-privilege policies for S3 and Snowflake access
- [x] Set up feature branch, activate virtual environment, and install AWS SDK packages (`boto3`)
- [x] Connect to S3 in Python and write upload script for unpacked JSON files
- [x] Document load script and update README
- [x] Ingest staged S3 data into Snowflake

#### Workflow Sketch:
<img width="90%" alt="Load workflow sketch" src="https://github.com/user-attachments/assets/f4bfe195-b63f-4ffc-b6e3-5cdd5ac0b849" />

### AWS S3 Staging & Security
Extracted JSON files are uploaded from local storage to an S3 staging bucket using `boto3`.
- **Encryption:** All uploads enforce server-side encryption via a customer-managed **AWS KMS key**.
- **Access Control:** Follows least-privilege IAM policies—Python uses write-only permissions for ingestion, while Snowflake uses a dedicated read-only IAM role via a Storage Integration.
- **Set Up:** Set up in AWS using the AWS CLI using `.json` scripts for the *iam python policy, iam snowflake policy* and *s3 bucket encryption.*

#### S3 bucket structure
```text
s3://bh-amplitude-storage/
└── python-import/
    └── YYYY-MM-DD_H.json
```
### Python Script:
The `load.py` script configures s3 credentials (stored in a `.env` file), configures file paths of unzipped data, and uploads each file to s3:
<img width="60%" alt="Python script sketch" src="https://github.com/user-attachments/assets/9386e5b2-09bb-4a61-a8c8-534870a113f4" />

### Snowflake: 
The raw data in S3 is then loaded into a Snowflake schema called **bh_amplitude_staging** through a script that uses the following steps:
- Create storage integration
- Create external stage
- Create empty table with a column for filename and a column for `.json`
- Copy from stage to table

The output from part two is a table called **bh_json_format** in the **bh_amplitude_staging** schema.



