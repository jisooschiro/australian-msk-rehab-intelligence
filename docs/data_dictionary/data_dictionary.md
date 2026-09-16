# Synthetic MSK Clinic Data Dictionary

## Purpose

This data dictionary defines the meaning, format, allowed values and validation requirements for each field in the synthetic MSK clinic dataset.

The dataset contains synthetic patient-level records created for research and portfolio purposes. It does not contain real patient or personally identifiable information.

## Dataset Tables

| Table | Unit of Record | Description |
|---|---|---|
| `patients` | One row per patient | Stores stable synthetic patient information |
| `episodes` | One row per treatment episode | Stores each course of care for an MSK condition |
| `appointments` | One row per appointment | Stores booking and attendance information |
| `outcome_assessments` | One row per assessment | Stores repeated patient outcome measurements |

## 1. Patients

**Unit of record:** One row per synthetic patient

The `patients` table stores basic patient information that is not specific to an individual treatment episode or appointment.

| Field | Definition | Data Type | Format / Allowed Values | Required | Key | Example |
|---|---|---|---|---|---|---|
| `patient_id` | Unique synthetic identifier assigned to each patient | string | `P` followed by four digits | Yes | PK | P0001 |
| `year_of_birth` | Synthetic year in which the patient was born | integer | 1920–2010 | Yes | - | 1986 |
| `sex` | Recorded sex category in the synthetic dataset | category | Female, Male, Intersex, Other, Not stated | Yes | - | Female |
| `registration_date` | Date the patient was first registered at the clinic | date | YYYY-MM-DD | Yes | - | 2026-01-10 |

### Patient Validation Rules

- `patient_id` must be unique and must not be null.
- `patient_id` must follow the format `P0001`.
- `year_of_birth` must be between 1920 and 2010.
- `sex` must match one of the defined allowed values.
- `registration_date` must follow the `YYYY-MM-DD` format.
- `registration_date` must not be in the future.

## 2. Episodes

**Unit of record:** One row per treatment episode

The `episodes` table stores each course of care provided to a patient for a primary MSK condition. One patient may have multiple treatment episodes over time.

| Field | Definition | Data Type | Format / Allowed Values | Required | Key | Example |
|---|---|---|---|---|---|---|
| `episode_id` | Unique identifier assigned to each treatment episode | string | `E` followed by four digits | Yes | PK | E0001 |
| `patient_id` | Identifier of the patient associated with the episode | string | Must exist in `patients.patient_id` | Yes | FK | P0001 |
| `condition_group` | Primary MSK condition category | category | Defined condition categories | Yes | - | Low back pain |
| `primary_body_region` | Primary body region treated during the episode | category | Defined body-region categories | Yes | - | Lumbar spine |
| `injury_mechanism` | Broad mechanism associated with the condition | category | Defined injury-mechanism categories | Yes | - | Lifting |
| `occupation_group_at_start` | Patient's occupation group at the beginning of the episode | category | Defined occupation categories | Yes | - | Healthcare |
| `physical_work_demand_at_start` | Physical demand of the patient's work at episode start | category | Sedentary, Light, Medium, Heavy, Very heavy | Yes | - | Heavy |
| `referral_source` | Source through which the patient entered the clinic | category | GP, Specialist, Employer, Insurer, Self-referral, Other | Yes | - | GP |
| `funding_source` | Primary funding arrangement for the episode | category | Private, Workers Compensation, CTP, Medicare, Other | Yes | - | Workers Compensation |
| `episode_start_date` | Date on which the treatment episode began | date | YYYY-MM-DD | Yes | - | 2026-01-10 |
| `episode_end_date` | Date on which the treatment episode ended | date | YYYY-MM-DD or null | No | - | 2026-03-21 |
| `discharge_reason` | Reason why the treatment episode ended | category | Goals met, Self-discharged, Referred elsewhere, No further contact, Funding ended, Other | No | - | Goals met |
| `rtw_status_at_start` | Return-to-work status at the start of treatment | category | Not working, Suitable duties, Reduced hours, Full duties | Yes | - | Not working |
| `rtw_status_at_end` | Return-to-work status at the end of treatment | category | Not working, Suitable duties, Reduced hours, Full duties, or null | No | - | Full duties |

### Episode Validation Rules

- `episode_id` must be unique and must not be null.
- `episode_id` must follow the format `E0001`.
- Every `patient_id` must exist in the `patients` table.
- `episode_start_date` must not be earlier than the patient's `registration_date`.
- `episode_end_date` may be null while treatment is ongoing.
- If recorded, `episode_end_date` must be on or after `episode_start_date`.
- `discharge_reason` and `rtw_status_at_end` may be null while treatment is ongoing.
- A completed episode must have an `episode_end_date` and a `discharge_reason`.

## 3. Appointments

**Unit of record:** One row per booked appointment

The `appointments` table stores scheduling and attendance information for each appointment. One treatment episode may include multiple appointments.

| Field | Definition | Data Type | Format / Allowed Values | Required | Key | Example |
|---|---|---|---|---|---|---|
| `appointment_id` | Unique identifier assigned to each appointment | string | `A` followed by four digits | Yes | PK | A0001 |
| `episode_id` | Identifier of the treatment episode associated with the appointment | string | Must exist in `episodes.episode_id` | Yes | FK | E0001 |
| `provider_id` | Anonymous identifier of the treating provider | string | `PR` followed by three digits | Yes | - | PR001 |
| `appointment_datetime` | Scheduled date and time of the appointment | datetime | YYYY-MM-DD HH:MM | Yes | - | 2026-01-15 10:30 |
| `booking_created_date` | Date on which the appointment was booked | date | YYYY-MM-DD | Yes | - | 2026-01-08 |
| `appointment_type` | Type of clinical appointment | category | Initial consultation, Follow-up, Progress review, Discharge review | Yes | - | Initial consultation |
| `attendance_status` | Final attendance result of the appointment | category | Attended, Cancelled, No-show | Yes | - | Attended |
| `duration_minutes` | Scheduled duration of the appointment in minutes | integer | Positive whole number | Yes | - | 30 |
| `cancellation_reason` | Recorded reason for a cancelled appointment | category | Illness, Work commitment, Family commitment, Transport issue, Financial reason, Rescheduled, Other, or null | No | - | Illness |

### Appointment Validation Rules

- `appointment_id` must be unique and must not be null.
- `appointment_id` must follow the format `A0001`.
- Every `episode_id` must exist in the `episodes` table.
- `provider_id` must follow the format `PR001`.
- `booking_created_date` must be on or before the appointment date.
- `appointment_datetime` must fall within the associated treatment episode.
- `duration_minutes` must be greater than zero.
- `cancellation_reason` is required when `attendance_status` is `Cancelled`.
- `cancellation_reason` must be null when `attendance_status` is `Attended` or `No-show`.

## 4. Outcome Assessments

**Unit of record:** One row per outcome assessment

The `outcome_assessments` table stores repeated clinical outcome measurements collected during a treatment episode, including baseline, progress and discharge assessments.

The scores are synthetic standardised measures created for this research prototype. They do not represent a specific validated clinical instrument.

| Field | Definition | Data Type | Format / Allowed Values | Required | Key | Example |
|---|---|---|---|---|---|---|
| `assessment_id` | Unique identifier assigned to each outcome assessment | string | `OA` followed by four digits | Yes | PK | OA0001 |
| `episode_id` | Identifier of the treatment episode associated with the assessment | string | Must exist in `episodes.episode_id` | Yes | FK | E0001 |
| `assessment_date` | Date on which the assessment was completed | date | YYYY-MM-DD | Yes | - | 2026-01-10 |
| `assessment_stage` | Stage of treatment at which the assessment was completed | category | Baseline, Progress, Discharge | Yes | - | Baseline |
| `pain_score` | Patient-reported pain score where a higher value indicates greater pain | integer | 0–10 | Yes | - | 7 |
| `adl_limitation_score` | Patient-reported limitation in activities of daily living where a higher value indicates greater limitation | integer | 0–10 | Yes | - | 6 |
| `function_score` | Synthetic functional outcome score where a higher value indicates better function | integer | 0–100 | Yes | - | 42 |
| `self_rated_recovery` | Patient-reported recovery score where a higher value indicates greater recovery | integer | 0–100 or null | No | - | 65 |
| `work_capacity` | Patient's work capacity at the time of assessment | category | No capacity, Partial capacity, Full capacity | Yes | - | Partial capacity |

### Outcome Assessment Validation Rules

- `assessment_id` must be unique and must not be null.
- `assessment_id` must follow the format `OA0001`.
- Every `episode_id` must exist in the `episodes` table.
- `assessment_date` must be on or after the associated `episode_start_date`.
- If the episode has ended, `assessment_date` must not be after `episode_end_date`.
- `pain_score` must be an integer between 0 and 10.
- `adl_limitation_score` must be an integer between 0 and 10.
- `function_score` must be an integer between 0 and 100.
- `self_rated_recovery` must be between 0 and 100 when recorded.
- `self_rated_recovery` may be null at baseline.

## Cross-Table Relationship Rules

- One patient may have zero or multiple treatment episodes.
- Each treatment episode must belong to exactly one patient.
- One treatment episode may have zero or multiple appointments.
- Each appointment must belong to exactly one treatment episode.
- One treatment episode may have zero or multiple outcome assessments.
- Each outcome assessment must belong to exactly one treatment episode.
- An episode cannot reference a patient that does not exist.
- An appointment or outcome assessment cannot reference an episode that does not exist.

## Derived Fields

The following fields will not be stored directly in the source tables. They will be calculated during data analysis.

| Derived Field | Calculation | Purpose |
|---|---|---|
| `age_at_episode_start` | Year of `episode_start_date` minus `year_of_birth` | Estimate patient age when treatment began |
| `episode_duration_days` | `episode_end_date` minus `episode_start_date` | Measure treatment episode duration |
| `booking_lead_days` | Appointment date minus `booking_created_date` | Measure how far in advance an appointment was booked |
| `pain_score_change` | Final `pain_score` minus baseline `pain_score` | Measure change in reported pain |
| `function_score_change` | Final `function_score` minus baseline `function_score` | Measure change in function |
| `adl_limitation_change` | Final `adl_limitation_score` minus baseline `adl_limitation_score` | Measure change in ADL limitation |
| `appointment_count` | Count of appointments per `episode_id` | Measure service utilisation |
| `no_show_count` | Count of appointments with `No-show` status per episode | Measure non-attendance |