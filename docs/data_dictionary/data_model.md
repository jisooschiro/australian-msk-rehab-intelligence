# Synthetic MSK Clinic Data Model

## 1. Patients

The `patients` table stores one row per synthetic patient.

It contains basic patient information that does not depend on a particular treatment episode or appointment.

| Column | Description | Example | Type | Key | Nullable |
|---|---|---|---|---|---|
| patient_id | Unique synthetic patient identifier | P0001 | string | PK | No |
| year_of_birth | Synthetic year of birth | 1986 | integer | - | No |
| sex | Recorded sex category | Female | category | - | No |
| registration_date | Date the patient was first registered at the clinic | 2026-01-10 | date | - | No |


## 2. Episodes

The `episodes` table stores one row per treatment episode.

A patient may have multiple treatment episodes over time. Each episode represents a course of care for one primary MSK condition.

| Column | Description | Example | Type | Key | Nullable |
|---|---|---|---|---|---|
| episode_id | Unique treatment episode identifier | E0001 | string | PK | No |
| patient_id | Patient associated with the episode | P0001 | string | FK | No |
| condition_group | Primary MSK condition category | Low back pain | category | - | No |
| primary_body_region | Primary body region being treated | Lumbar spine | category | - | No |
| injury_mechanism | Broad mechanism associated with the condition | Work-related lifting | category | - | No |
| occupation_group_at_start | Occupation group at the start of the episode | Healthcare worker | category | - | No |
| physical_work_demand_at_start | Physical demand of the patient's work | Heavy | category | - | Yes |
| referral_source | Source through which the patient entered the clinic | GP | category | - | No |
| funding_source | Primary funding type for the episode | Workers Compensation | category | - | No |
| episode_start_date | Date the treatment episode began | 2026-01-10 | date | - | No |
| episode_end_date | Date the treatment episode ended | 2026-03-21 | date | - | Yes |
| discharge_reason | Reason the treatment episode ended | Goals met | category | - | Yes |
| rtw_status_at_start | Return-to-work status at the start | Not working | category | - | No |
| rtw_status_at_end | Return-to-work status at the end | Full duties | category | - | Yes |

## 3. Appointments

The `appointments` table stores one row per booked appointment.

Each appointment belongs to one treatment episode. A treatment episode may include multiple appointments.

| Column | Description | Example | Type | Key | Nullable |
|---|---|---|---|---|---|
| appointment_id | Unique appointment identifier | A0001 | string | PK | No |
| episode_id | Treatment episode associated with the appointment | E0001 | string | FK | No |
| provider_id | Anonymous identifier of the treating provider | PR001 | string | - | No |
| appointment_datetime | Scheduled date and time of the appointment | 2026-01-15 10:30 | datetime | - | No |
| booking_created_date | Date the appointment was booked | 2026-01-08 | date | - | No |
| appointment_type | Type of appointment | Initial consultation | category | - | No |
| attendance_status | Final attendance result | Attended | category | - | No |
| duration_minutes | Scheduled appointment duration in minutes | 30 | integer | - | No |
| cancellation_reason | Reason the appointment was cancelled | Illness | category | - | Yes |

## 4. Outcome Assessments

The `outcome_assessments` table stores one row per clinical outcome assessment.

Each treatment episode may include multiple assessments, such as baseline, progress and discharge assessments.

The scores are synthetic standardised measures created for this research prototype. They do not represent a specific validated clinical instrument.

| Column | Description | Example | Type | Key | Nullable |
|---|---|---|---|---|---|
| assessment_id | Unique outcome assessment identifier | OA0001 | string | PK | No |
| episode_id | Treatment episode associated with the assessment | E0001 | string | FK | No |
| assessment_date | Date the outcome assessment was completed | 2026-01-10 | date | - | No |
| assessment_stage | Stage of the treatment episode | Baseline | category | - | No |
| pain_score | Patient-reported pain score from 0 to 10, where a higher score indicates greater pain | 7 | integer | - | No |
| adl_limitation_score | Patient-reported ADL limitation score from 0 to 10, where a higher score indicates greater limitation | 6 | integer | - | No |
| function_score | Synthetic functional outcome score from 0 to 100, where a higher score indicates better function | 42 | integer | - | No |
| self_rated_recovery | Patient-reported recovery score from 0 to 100, where a higher score indicates greater recovery | 65 | integer | - | Yes |
| work_capacity | Patient's current work capacity | Partial capacity | category | - | No |






## Allowed Category Values

### Patients

- `sex`: Female, Male, Intersex, Other, Not stated

### Episodes

- `condition_group`: Low back pain, Neck pain, Shoulder condition, Elbow condition, Wrist or hand condition, Hip condition, Knee condition, Ankle or foot condition, Multiple regions, Other
- `primary_body_region`: Cervical spine, Thoracic spine, Lumbar spine, Shoulder, Elbow, Wrist or hand, Hip, Knee, Ankle or foot, Multiple regions, Other
- `injury_mechanism`: Lifting, Repetitive activity, Fall, Collision, Sports activity, Motor vehicle accident, Gradual onset, Other
- `occupation_group_at_start`: Healthcare, Construction, Manufacturing, Transport, Office or administration, Retail or hospitality, Education, Trades, Not currently employed, Other
- `physical_work_demand_at_start`: Sedentary, Light, Medium, Heavy, Very heavy
- `referral_source`: GP, Specialist, Employer, Insurer, Self-referral, Other
- `funding_source`: Private, Workers Compensation, CTP, Medicare, Other
- `discharge_reason`: Goals met, Self-discharged, Referred elsewhere, No further contact, Funding ended, Other
- `rtw_status_at_start`: Not working, Suitable duties, Reduced hours, Full duties
- `rtw_status_at_end`: Not working, Suitable duties, Reduced hours, Full duties

### Appointments

- `appointment_type`: Initial consultation, Follow-up, Progress review, Discharge review
- `attendance_status`: Attended, Cancelled, No-show
- `cancellation_reason`: Illness, Work commitment, Family commitment, Transport issue, Financial reason, Rescheduled, Other

### Outcome Assessments

- `assessment_stage`: Baseline, Progress, Discharge
- `work_capacity`: No capacity, Partial capacity, Full capacity






## Validation Rules

### Patients

- `year_of_birth` must be between 1920 and 2010.
- `registration_date` must not be in the future.
- Each `patient_id` must be unique and must not be null.

### Episodes

- Each `episode_id` must be unique and must not be null.
- Every `patient_id` must exist in the `patients` table.
- `episode_end_date` may be null for an ongoing episode.
- If present, `episode_end_date` must be on or after `episode_start_date`.
- `discharge_reason` and `rtw_status_at_end` may be null while an episode is ongoing.

### Appointments

- Each `appointment_id` must be unique and must not be null.
- Every `episode_id` must exist in the `episodes` table.
- `booking_created_date` must be on or before the appointment date.
- `duration_minutes` must be greater than zero.
- `cancellation_reason` is required only when `attendance_status` is `Cancelled`.
- `cancellation_reason` must be null when `attendance_status` is `Attended` or `No-show`.

### Outcome Assessments

- Each `assessment_id` must be unique and must not be null.
- Every `episode_id` must exist in the `episodes` table.
- `assessment_date` must fall on or after the episode start date.
- `pain_score` must be between 0 and 10.
- `adl_limitation_score` must be between 0 and 10.
- `function_score` must be between 0 and 100.
- `self_rated_recovery` must be between 0 and 100 when recorded.
- `self_rated_recovery` may be null at baseline.