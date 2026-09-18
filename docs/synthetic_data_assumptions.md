# Synthetic Data Generation Assumptions

## Purpose

This document defines the assumptions that will be used to generate synthetic patient-level data for the Australian MSK clinic analytics prototype.

The assumptions are informed by Australian public data and clinical workflow knowledge. They are not intended to reproduce the Australian population or any real clinic exactly.

## Evidence and Assumption Levels

Each generation rule will be classified using one of the following evidence levels:

| Evidence Level | Meaning |
|---|---|
| Public evidence | Directly supported by an Australian public source |
| Evidence-informed assumption | Informed by public evidence but adjusted for the scope of this synthetic MSK clinic |
| Project assumption | Selected for analytical usefulness where no suitable public clinic-level statistic is available |

## Australian Context

| Finding | Project Relevance | Source |
|---|---|---|
| Around 29% of people in Australia were estimated to be living with chronic musculoskeletal conditions | Confirms that MSK conditions represent a substantial Australian health burden | AIHW |
| Around 16% of people in Australia were estimated to be living with back problems in 2022 | Supports including back conditions as a major condition group | AIHW |
| Back problem prevalence increases with age | Supports linking age with the probability of some chronic conditions | AIHW |
| Workers' compensation and return-to-work datasets are available nationally | Supports including funding source, occupation and RTW fields | Safe Work Australia |

## Important Limitation

Population prevalence is not the same as the condition distribution within an MSK clinic.

Public statistics will therefore be used to inform the synthetic data, but clinic-level probabilities will be clearly labelled as project assumptions.

## Patient Generation Assumptions

### Age at Registration

The synthetic clinic will primarily represent an adult working-age population while retaining a smaller number of younger and older patients.

| Age Group | Generation Probability | Evidence Level | Rationale |
|---|---:|---|---|
| 18–24 | 8% | Project assumption | Younger adults are included but are expected to represent a smaller proportion of the clinic population |
| 25–34 | 18% | Evidence-informed assumption | Represents working-age adults with occupational, lifestyle and sports-related MSK conditions |
| 35–44 | 22% | Evidence-informed assumption | Represents a major working-age group relevant to occupational MSK care |
| 45–54 | 24% | Evidence-informed assumption | Assigned the highest probability because MSK burden generally increases with age while patients remain strongly relevant to RTW analysis |
| 55–64 | 18% | Evidence-informed assumption | Represents older working-age adults with increasing chronic and degenerative MSK conditions |
| 65–74 | 8% | Project assumption | Included for non-occupational and chronic MSK presentations |
| 75–85 | 2% | Project assumption | Included in a limited proportion because the initial prototype focuses primarily on working-age rehabilitation |

**Total: 100%**

### Age Generation Rule

- Generate `age_at_registration` using the age-group probabilities above.
- Calculate `year_of_birth` from `registration_date` and the generated age.
- Do not store `age_at_registration` in `patients.csv`.
- Recalculate age during analysis when required.
- All synthetic patients must be at least 18 years old at registration.

### Recorded Sex

The synthetic dataset will include several recorded sex categories. These probabilities are project assumptions and are not intended to estimate the prevalence of sex categories in the Australian population.

| Recorded Sex | Generation Probability | Evidence Level |
|---|---:|---|
| Female | 50% | Project assumption |
| Male | 48% | Project assumption |
| Intersex | 0.5% | Project assumption |
| Other | 0.5% | Project assumption |
| Not stated | 1% | Project assumption |

**Total: 100%**

### Sex Generation Rules

- Use only the values defined in the data dictionary.
- Do not infer gender identity from recorded sex.
- Do not create different treatment outcomes solely based on sex.
- These values are included to support demographic analysis, not clinical decision-making.

### Number of Episodes per Patient

A patient may have no treatment episode or may return to the clinic for multiple separate episodes of care.

| Number of Episodes | Generation Probability | Evidence Level | Interpretation |
|---:|---:|---|---|
| 0 | 5% | Project assumption | Registered patient with no commenced treatment episode |
| 1 | 70% | Project assumption | Patient attended for one course of care |
| 2 | 20% | Project assumption | Patient returned for a separate course of care |
| 3 | 5% | Project assumption | Patient had three separate courses of care |

**Total: 100%**

### Episode Count Rules

- Each episode must have a unique `episode_id`.
- Every episode must reference an existing `patient_id`.
- Multiple episodes for the same patient must represent separate courses of care.
- Episode date ranges for the same patient must not overlap.
- A new episode may have a different condition, occupation or work-demand category.

## Episode Generation Assumptions

### Primary Condition Group

The following probabilities define the primary condition recorded for each synthetic treatment episode.

These values are evidence-informed assumptions designed for an outpatient MSK clinic prototype. They do not represent the exact condition distribution of Australian MSK clinics.

| Condition Group | Generation Probability | Evidence Level |
|---|---:|---|
| Low back pain | 28% | Evidence-informed assumption |
| Neck pain | 12% | Evidence-informed assumption |
| Shoulder condition | 15% | Project assumption |
| Knee condition | 15% | Project assumption |
| Ankle or foot condition | 8% | Project assumption |
| Hip condition | 7% | Project assumption |
| Wrist or hand condition | 5% | Project assumption |
| Elbow condition | 4% | Project assumption |
| Multiple regions | 4% | Project assumption |
| Other | 2% | Project assumption |

**Total: 100%**

### Condition and Body-Region Mapping

The primary body region must be consistent with the selected condition group.

| Condition Group | Primary Body Region |
|---|---|
| Low back pain | Lumbar spine |
| Neck pain | Cervical spine |
| Shoulder condition | Shoulder |
| Elbow condition | Elbow |
| Wrist or hand condition | Wrist or hand |
| Hip condition | Hip |
| Knee condition | Knee |
| Ankle or foot condition | Ankle or foot |
| Multiple regions | Multiple regions |
| Other | Other |

### Condition Generation Rules

- Each treatment episode must have one primary condition group.
- The `primary_body_region` must match the selected `condition_group`.
- Secondary conditions will not be generated in v0.1.
- `Low back pain` will be the most common condition in the synthetic clinic.
- The condition probabilities must total 100%.

### Occupation Group

The occupation distribution is a project assumption designed to include a mixture of sedentary, service-based and physically demanding work.

| Occupation Group | Generation Probability | Most Likely Work Demands |
|---|---:|---|
| Office or administration | 18% | Sedentary, Light |
| Construction | 13% | Heavy, Very heavy |
| Healthcare | 12% | Medium, Heavy |
| Retail or hospitality | 12% | Light, Medium |
| Manufacturing | 10% | Medium, Heavy |
| Transport | 10% | Sedentary, Medium, Heavy |
| Education | 8% | Light, Medium |
| Trades | 8% | Medium, Heavy, Very heavy |
| Not currently employed | 5% | Not applicable |
| Other | 4% | Light, Medium |

**Total: 100%**

### Occupation and Work-Demand Rules

- `physical_work_demand_at_start` must be plausible for the selected occupation group.
- Construction and trade occupations will have a higher probability of `Heavy` or `Very heavy` work.
- Office or administration occupations will have a higher probability of `Sedentary` work.
- Healthcare occupations may include `Medium` or `Heavy` physical demand.
- Transport occupations may range from `Sedentary` driving work to `Heavy` manual-handling work.
- `physical_work_demand_at_start` will be null when the occupation group is `Not currently employed`.

### Injury Mechanism

The injury mechanism will be generated using the following project assumptions.

| Injury Mechanism | Generation Probability | Evidence Level |
|---|---:|---|
| Gradual or non-specific onset | 28% | Evidence-informed assumption |
| Manual handling or lifting | 20% | Evidence-informed assumption |
| Repetitive movement or overuse | 15% | Evidence-informed assumption |
| Sports or exercise | 12% | Project assumption |
| Slip, trip or fall | 10% | Evidence-informed assumption |
| Motor vehicle accident | 7% | Project assumption |
| Direct impact | 5% | Project assumption |
| Other | 3% | Project assumption |

**Total: 100%**

### Injury-Mechanism Generation Rules

- The injury mechanism must be plausible for the selected occupation and physical work demand.
- `Manual handling or lifting` will have a higher probability for `Construction`, `Healthcare`, `Manufacturing`, `Transport` and `Trades`.
- `Repetitive movement or overuse` may occur across office, service-based and physically demanding occupations.
- `Gradual or non-specific onset` may occur in any occupation group.
- `Sports or exercise` is not determined by occupation group.
- `Slip, trip or fall`, `Motor vehicle accident` and `Direct impact` may occur in any occupation group.
- Patients who are `Not currently employed` must not be assigned a work-related injury solely based on occupation.
- The injury mechanism must not be selected independently when conditional rules apply.

### Referral Source

The following probabilities define how patients are referred to the synthetic clinic.

| Referral Source | Generation Probability | Evidence Level |
|---|---:|---|
| General practitioner | 35% | Evidence-informed assumption |
| Self-referral | 30% | Project assumption |
| Specialist | 10% | Project assumption |
| Employer | 8% | Project assumption |
| Insurer or case manager | 7% | Project assumption |
| Other allied-health provider | 7% | Project assumption |
| Other | 3% | Project assumption |

**Total: 100%**

### Funding Source

The following probabilities define the primary funding source for each treatment episode.

| Funding Source | Generation Probability | Evidence Level |
|---|---:|---|
| Private health insurance | 32% | Project assumption |
| Self-funded | 28% | Project assumption |
| Workers' compensation | 18% | Evidence-informed assumption |
| Medicare-supported care | 10% | Project assumption |
| Compulsory third-party insurance | 7% | Project assumption |
| Department of Veterans' Affairs | 2% | Project assumption |
| Other | 3% | Project assumption |

**Total: 100%**

### Referral and Funding Rules

- Each treatment episode must have one referral source and one primary funding source.
- Referral source and funding source must not be generated as if they were completely independent.
- Episodes funded through `Workers' compensation` will have a higher probability of referral from an `Employer`, `Insurer or case manager`, or `General practitioner`.
- Episodes funded through `Compulsory third-party insurance` will have a higher probability of an injury mechanism recorded as `Motor vehicle accident`.
- `Self-referral` will have a higher probability of being `Self-funded` or funded through `Private health insurance`.
- `Medicare-supported care` will have a higher probability of referral from a `General practitioner`.
- `Department of Veterans' Affairs` funding will represent only a small proportion of episodes.
- Funding source must not be inferred solely from the patient's age, sex or condition.

### Episode Status

| Episode Status | Generation Probability | Evidence Level |
|---|---:|---|
| Completed | 65% | Project assumption |
| Active | 25% | Project assumption |
| Discontinued | 10% | Project assumption |

**Total: 100%**

### Episode Duration

Episode duration will depend partly on the condition, injury mechanism and episode status.

| Episode Duration | Generation Probability | Evidence Level |
|---|---:|---|
| 1–14 days | 10% | Project assumption |
| 15–42 days | 30% | Project assumption |
| 43–84 days | 35% | Project assumption |
| 85–168 days | 20% | Project assumption |
| 169–365 days | 5% | Project assumption |

**Total: 100%**

### Discharge Reason

The discharge reason will be generated only for episodes that are no longer active.

| Discharge Reason | Generation Probability | Evidence Level |
|---|---:|---|
| Goals achieved | 55% | Project assumption |
| Patient discontinued | 15% | Project assumption |
| Referred to another provider | 10% | Project assumption |
| No further improvement | 8% | Project assumption |
| Lost to follow-up | 8% | Project assumption |
| Other | 4% | Project assumption |

**Total: 100%**

### Episode Date and Status Rules

- `episode_start_date` must be on or after the patient's `registration_date`.
- `episode_end_date` must not be earlier than `episode_start_date`.
- `episode_end_date` must be null when `episode_status` is `Active`.
- `discharge_reason` must be null when `episode_status` is `Active`.
- `episode_end_date` and `discharge_reason` are required for `Completed` and `Discontinued` episodes.
- Episodes for the same patient must not have overlapping date ranges.
- The generated episode duration must not exceed 365 days in v0.1.
- Longer durations will be more likely for gradual-onset or chronic conditions.
- Shorter durations will be more likely for minor acute conditions.

### Return-to-Work Status at Episode Start

The return-to-work status at the beginning of an episode will be generated only for employed patients.

| RTW Status at Start | Generation Probability | Evidence Level |
|---|---:|---|
| Full duties | 40% | Project assumption |
| Modified duties | 20% | Evidence-informed assumption |
| Reduced hours | 15% | Evidence-informed assumption |
| Not working | 25% | Evidence-informed assumption |

**Total: 100%**

### Return-to-Work Status at Episode End

The end status will be generated conditionally from the patient's starting status, clinical progress and episode outcome.

Possible values are:

- `Full duties`
- `Modified duties`
- `Reduced hours`
- `Not working`
- `Not applicable`

### Return-to-Work Generation Rules

- RTW status must be `Not applicable` when `occupation_group_at_start` is `Not currently employed`.
- Employed patients must not have an RTW status of `Not applicable`.
- `rtw_status_at_end` must be null while the episode is `Active`.
- `rtw_status_at_end` is required for completed or discontinued episodes involving employed patients.
- The end status must be generated from the start status rather than selected independently.
- Improvement will be more likely when pain decreases, function improves and the episode is completed.
- Patients who start on `Modified duties`, `Reduced hours` or `Not working` may progress to `Full duties`.
- Patients may remain at the same work status when improvement is limited.
- A small proportion of patients may have a worse RTW status at the end.
- RTW improvement must not be guaranteed solely because treatment was completed.

## Appointment Generation Assumptions

### Number of Appointments per Episode

| Number of Appointments | Generation Probability | Evidence Level |
|---|---:|---|
| 1–3 | 15% | Project assumption |
| 4–6 | 35% | Project assumption |
| 7–10 | 30% | Project assumption |
| 11–15 | 15% | Project assumption |
| 16–20 | 5% | Project assumption |

**Total: 100%**

### Attendance Status

| Attendance Status | Generation Probability | Evidence Level |
|---|---:|---|
| Attended | 82% | Project assumption |
| Cancelled | 12% | Project assumption |
| No-show | 6% | Project assumption |

**Total: 100%**

### Cancellation Reason

A cancellation reason will be generated only when the attendance status is `Cancelled`.

| Cancellation Reason | Generation Probability | Evidence Level |
|---|---:|---|
| Illness | 25% | Project assumption |
| Work commitment | 20% | Project assumption |
| Personal or family reason | 20% | Project assumption |
| Transport difficulty | 10% | Project assumption |
| Schedule conflict | 15% | Project assumption |
| Other | 10% | Project assumption |

**Total: 100%**

### Appointment Generation Rules

- Every appointment must reference an existing `episode_id`.
- The appointment date must fall within the episode's date range.
- Appointments for the same episode must follow chronological order.
- Completed episodes will generally have more appointments than recently started active episodes.
- `attendance_status` must be one of `Attended`, `Cancelled` or `No-show`.
- `cancellation_reason` is required when `attendance_status` is `Cancelled`.
- `cancellation_reason` must be null when the status is `Attended` or `No-show`.
- A `No-show` means that the patient did not attend and did not cancel beforehand.
- The appointment creation date must not be later than the appointment date.
- Multiple appointments for the same episode must not occur at the same date and time.

## Outcome Assessment Generation Assumptions

### Number of Assessments per Episode

| Number of Assessments | Generation Probability | Evidence Level |
|---|---:|---|
| 1 | 20% | Project assumption |
| 2 | 45% | Project assumption |
| 3 | 25% | Project assumption |
| 4 or more | 10% | Project assumption |

**Total: 100%**

### Assessment Timing

Outcome assessments may be recorded at the following stages:

- Initial assessment near the beginning of the episode
- Progress assessment during treatment
- Final assessment near the end of a completed episode

### Outcome Score Rules

- `pain_score` must be between 0 and 10.
- `adl_limitation_score` must be between 0 and 10.
- `function_score` must remain within the range defined in the data dictionary.
- `self_rated_recovery` must remain within the range defined in the data dictionary.
- Higher `pain_score` values represent more severe pain.
- Higher `adl_limitation_score` values represent greater difficulty with daily activities.
- Higher `function_score` values represent better physical function.
- Higher `self_rated_recovery` values represent greater perceived recovery.
- Scores must use whole numbers in v0.1.

### Outcome Change Assumptions

| Outcome Pattern | Generation Probability | Evidence Level |
|---|---:|---|
| Clear improvement | 60% | Project assumption |
| Small improvement | 20% | Project assumption |
| Little or no change | 15% | Project assumption |
| Deterioration | 5% | Project assumption |

**Total: 100%**

### Outcome Assessment Rules

- Every assessment must reference an existing `episode_id`.
- The assessment date must fall within the episode's date range.
- Assessments for the same episode must follow chronological order.
- The first assessment should occur near the beginning of the episode.
- Completed episodes should usually have both an initial and a final assessment.
- Active episodes may have an initial assessment without a final assessment.
- Discontinued episodes may have missing final outcome measures.
- Pain and ADL limitation will generally decrease when a patient improves.
- Function and self-rated recovery will generally increase when a patient improves.
- Outcome improvement must not be guaranteed for every episode.
- Changes between assessments should be gradual and remain within the permitted score ranges.
- Outcome scores must not be generated independently when representing the same patient's progress.
- `work_capacity` must be consistent with the patient's RTW status.
- `work_capacity` must be `Not applicable` when the patient is not currently employed.
