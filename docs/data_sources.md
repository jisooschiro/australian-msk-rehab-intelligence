# Data Sources and Synthetic Data Principles

## Patient-Level Data

All patient-level records used in this project will be synthetically generated.

The project does not use real patient records, clinical notes, names, contact details, claim numbers or other personally identifiable information.

The synthetic dataset will contain four linked CSV files:

- `patients.csv`
- `episodes.csv`
- `appointments.csv`
- `outcome_assessments.csv`

## Australian Public Data Sources

Australian public data may be used to inform selected assumptions and provide real-world context.

Planned reference sources include:

| Organisation | Intended Use |
|---|---|
| Australian Institute of Health and Welfare (AIHW) | General context about musculoskeletal conditions in Australia |
| Safe Work Australia | Context about work-related MSK conditions, occupation and return-to-work |
| Australian Bureau of Statistics (ABS) | General demographic and occupation context |

These sources will not be treated as patient-level clinic records.

## Synthetic Data Generation Principles

- No real patient data will be copied into the dataset.
- All identifiers will be artificially generated.
- Names, addresses, phone numbers and email addresses will not be included.
- The dataset will follow the relationships and validation rules defined in the project documentation.
- Generated values will remain plausible without representing real individuals.
- Assumptions used during data generation will be documented.
- Synthetic data limitations will be stated clearly in project outputs.

## Intended Use

The synthetic dataset is intended for:

- Python and pandas data analysis
- SQL and MySQL practice
- Power BI dashboard development
- Machine-learning experimentation in later project stages
- Portfolio demonstration

It is not intended for diagnosis, treatment recommendations or independent clinical decision-making.
