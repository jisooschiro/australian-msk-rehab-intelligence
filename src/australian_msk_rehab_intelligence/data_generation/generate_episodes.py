from pathlib import Path

import numpy as np
import pandas as pd


# Define project paths
PROJECT_ROOT = Path(__file__).resolve().parents[3]
PATIENTS_PATH = PROJECT_ROOT / "data" / "synthetic" / "patients.csv"
EPISODES_PATH = PROJECT_ROOT / "data" / "synthetic" / "episodes.csv"

# Define generation settings
RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)

# Load the synthetic patient data
patients_df = pd.read_csv(
    PATIENTS_PATH,
    parse_dates=["registration_date"],
)

print(patients_df.head())
print("Number of patients:", len(patients_df))


# Define episode-count probabilities per patient
EPISODE_COUNT_VALUES = [0, 1, 2, 3]
EPISODE_COUNT_PROBABILITIES = [0.05, 0.70, 0.20, 0.05]

# Generate the number of episodes for each patient
episode_counts = rng.choice(
    EPISODE_COUNT_VALUES,
    size=len(patients_df),
    p=EPISODE_COUNT_PROBABILITIES,
)

# Create the initial episode records
episode_records = []
episode_number = 1

for patient_id, episode_count in zip(
    patients_df["patient_id"],
    episode_counts,
):
    for _ in range(episode_count):
        episode_records.append({
            "episode_id": f"E{episode_number:05d}",
            "patient_id": patient_id,
        })

        episode_number += 1

# Create the initial episode DataFrame
episodes_df = pd.DataFrame(episode_records)

print(episodes_df.head())
print("Number of episodes:", len(episodes_df))

# Validate episode identifiers and patient references
print(
    "Duplicate episode IDs:",
    episodes_df["episode_id"].duplicated().sum(),
)

print(
    "Invalid patient references:",
    (~episodes_df["patient_id"].isin(patients_df["patient_id"])).sum(),
)

print(
    "Episode count per patient:"
)

print(
    pd.Series(episode_counts)
    .value_counts()
    .sort_index()
)

# Define primary condition probabilities
CONDITION_PROBABILITIES = {
    "Low back pain": 0.28,
    "Neck pain": 0.12,
    "Shoulder condition": 0.15,
    "Knee condition": 0.15,
    "Ankle or foot condition": 0.08,
    "Hip condition": 0.07,
    "Wrist or hand condition": 0.05,
    "Elbow condition": 0.04,
    "Multiple regions": 0.04,
    "Other": 0.02,
}

# Map each condition to its corresponding body region
CONDITION_BODY_REGION_MAP = {
    "Low back pain": "Lumbar spine",
    "Neck pain": "Cervical spine",
    "Shoulder condition": "Shoulder",
    "Knee condition": "Knee",
    "Ankle or foot condition": "Ankle or foot",
    "Hip condition": "Hip",
    "Wrist or hand condition": "Wrist or hand",
    "Elbow condition": "Elbow",
    "Multiple regions": "Multiple regions",
    "Other": "Other",
}

# Generate one primary condition for each episode
episodes_df["condition_group"] = rng.choice(
    list(CONDITION_PROBABILITIES.keys()),
    size=len(episodes_df),
    p=list(CONDITION_PROBABILITIES.values()),
)

# Assign the matching body region
episodes_df["primary_body_region"] = (
    episodes_df["condition_group"]
    .map(CONDITION_BODY_REGION_MAP)
)

# Check the generated condition distribution
print(
    episodes_df["condition_group"]
    .value_counts(normalize=True)
    .round(3)
)

# Validate condition and body-region combinations
expected_body_regions = (
    episodes_df["condition_group"]
    .map(CONDITION_BODY_REGION_MAP)
)

invalid_body_region_count = (
    episodes_df["primary_body_region"]
    != expected_body_regions
).sum()

print(
    "Invalid condition-body region combinations:",
    invalid_body_region_count,
)

print(
    episodes_df[
        [
            "episode_id",
            "patient_id",
            "condition_group",
            "primary_body_region",
        ]
    ].head()
)

# Define occupation-group probabilities
OCCUPATION_PROBABILITIES = {
    "Office or administration": 0.18,
    "Construction": 0.13,
    "Healthcare": 0.12,
    "Retail or hospitality": 0.12,
    "Manufacturing": 0.10,
    "Transport": 0.10,
    "Education": 0.08,
    "Trades": 0.08,
    "Not currently employed": 0.05,
    "Other": 0.04,
}

# Define work-demand probabilities by occupation group
WORK_DEMAND_BY_OCCUPATION = {
    "Office or administration": {
        "Sedentary": 0.75,
        "Light": 0.25,
    },
    "Construction": {
        "Medium": 0.20,
        "Heavy": 0.55,
        "Very heavy": 0.25,
    },
    "Healthcare": {
        "Light": 0.15,
        "Medium": 0.55,
        "Heavy": 0.30,
    },
    "Retail or hospitality": {
        "Light": 0.40,
        "Medium": 0.60,
    },
    "Manufacturing": {
        "Medium": 0.55,
        "Heavy": 0.45,
    },
    "Transport": {
        "Sedentary": 0.45,
        "Medium": 0.35,
        "Heavy": 0.20,
    },
    "Education": {
        "Light": 0.65,
        "Medium": 0.35,
    },
    "Trades": {
        "Medium": 0.25,
        "Heavy": 0.55,
        "Very heavy": 0.20,
    },
    "Other": {
        "Light": 0.50,
        "Medium": 0.50,
    },
}

# Generate an occupation group for each episode
episodes_df["occupation_group_at_start"] = rng.choice(
    list(OCCUPATION_PROBABILITIES.keys()),
    size=len(episodes_df),
    p=list(OCCUPATION_PROBABILITIES.values()),
)

# Generate a plausible work demand for an occupation group
def generate_work_demand(occupation_group):
    if occupation_group == "Not currently employed":
        return None

    demand_probabilities = WORK_DEMAND_BY_OCCUPATION[
        occupation_group
    ]

    return rng.choice(
        list(demand_probabilities.keys()),
        p=list(demand_probabilities.values()),
    )

# Generate work demand conditionally from occupation group
episodes_df["physical_work_demand_at_start"] = [
    generate_work_demand(occupation_group)
    for occupation_group
    in episodes_df["occupation_group_at_start"]
]

# Generate work demand conditionally from occupation group
episodes_df["physical_work_demand_at_start"] = [
    generate_work_demand(occupation_group)
    for occupation_group
    in episodes_df["occupation_group_at_start"]
]

# Define base injury-mechanism probabilities
BASE_INJURY_MECHANISM_PROBABILITIES = {
    "Gradual or non-specific onset": 0.28,
    "Manual handling or lifting": 0.20,
    "Repetitive movement or overuse": 0.15,
    "Sports or exercise": 0.12,
    "Slip, trip or fall": 0.10,
    "Motor vehicle accident": 0.07,
    "Direct impact": 0.05,
    "Other": 0.03,
}

# Generate an injury mechanism based on occupation and work demand
def generate_injury_mechanism(
    occupation_group,
    work_demand,
):
    weights = BASE_INJURY_MECHANISM_PROBABILITIES.copy()

    manual_occupations = {
        "Construction",
        "Healthcare",
        "Manufacturing",
        "Transport",
        "Trades",
    }

    if occupation_group in manual_occupations:
        weights["Manual handling or lifting"] *= 1.8

    if work_demand in {"Heavy", "Very heavy"}:
        weights["Manual handling or lifting"] *= 1.5
        weights["Direct impact"] *= 1.3

    if work_demand == "Sedentary":
        weights["Gradual or non-specific onset"] *= 1.5
        weights["Repetitive movement or overuse"] *= 1.4

    if occupation_group == "Office or administration":
        weights["Repetitive movement or overuse"] *= 1.4

    if occupation_group == "Not currently employed":
        weights["Manual handling or lifting"] *= 0.5
        weights["Repetitive movement or overuse"] *= 0.7
        weights["Gradual or non-specific onset"] *= 1.4

    mechanisms = list(weights.keys())
    probabilities = np.array(
        list(weights.values()),
        dtype=float,
    )

    probabilities = probabilities / probabilities.sum()

    return rng.choice(
        mechanisms,
        p=probabilities,
    )

# Generate injury mechanisms conditionally
episodes_df["injury_mechanism"] = [
    generate_injury_mechanism(
        occupation_group,
        work_demand,
    )
    for occupation_group, work_demand in zip(
        episodes_df["occupation_group_at_start"],
        episodes_df["physical_work_demand_at_start"],
    )
]

# Check the overall injury-mechanism distribution
print(
    episodes_df["injury_mechanism"]
    .value_counts(normalize=True)
    .round(3)
)

# Compare injury mechanisms across occupation groups
print(
    pd.crosstab(
        episodes_df["occupation_group_at_start"],
        episodes_df["injury_mechanism"],
        normalize="index",
    )
    .round(2)
)

# Validate injury-mechanism values
allowed_injury_mechanisms = set(
    BASE_INJURY_MECHANISM_PROBABILITIES.keys()
)

invalid_injury_mechanism_count = (
    ~episodes_df["injury_mechanism"]
    .isin(allowed_injury_mechanisms)
).sum()

print(
    "Invalid injury mechanisms:",
    invalid_injury_mechanism_count,
)

# Define base funding-source probabilities
BASE_FUNDING_PROBABILITIES = {
    "Private health insurance": 0.32,
    "Self-funded": 0.28,
    "Workers' compensation": 0.18,
    "Medicare-supported care": 0.10,
    "Compulsory third-party insurance": 0.07,
    "Department of Veterans' Affairs": 0.02,
    "Other": 0.03,
}

# Generate a funding source from episode characteristics
def generate_funding_source(
    injury_mechanism,
    occupation_group,
):
    weights = BASE_FUNDING_PROBABILITIES.copy()

    if injury_mechanism == "Motor vehicle accident":
        weights["Compulsory third-party insurance"] *= 5.0

    if (
        occupation_group != "Not currently employed"
        and injury_mechanism
        in {
            "Manual handling or lifting",
            "Repetitive movement or overuse",
            "Slip, trip or fall",
            "Direct impact",
        }
    ):
        weights["Workers' compensation"] *= 1.8

    if occupation_group == "Not currently employed":
        weights["Workers' compensation"] *= 0.2
        weights["Self-funded"] *= 1.2
        weights["Medicare-supported care"] *= 1.3

    funding_sources = list(weights.keys())
    probabilities = np.array(
        list(weights.values()),
        dtype=float,
    )

    probabilities = probabilities / probabilities.sum()

    return rng.choice(
        funding_sources,
        p=probabilities,
    )

# Generate funding sources conditionally
episodes_df["funding_source"] = [
    generate_funding_source(
        injury_mechanism,
        occupation_group,
    )
    for injury_mechanism, occupation_group in zip(
        episodes_df["injury_mechanism"],
        episodes_df["occupation_group_at_start"],
    )
]

# Generate funding sources conditionally
episodes_df["funding_source"] = [
    generate_funding_source(
        injury_mechanism,
        occupation_group,
    )
    for injury_mechanism, occupation_group in zip(
        episodes_df["injury_mechanism"],
        episodes_df["occupation_group_at_start"],
    )
]

# Define base referral-source probabilities
BASE_REFERRAL_PROBABILITIES = {
    "General practitioner": 0.35,
    "Self-referral": 0.30,
    "Specialist": 0.10,
    "Employer": 0.08,
    "Insurer or case manager": 0.07,
    "Other allied-health provider": 0.07,
    "Other": 0.03,
}

# Generate a referral source from the funding source
def generate_referral_source(funding_source):
    weights = BASE_REFERRAL_PROBABILITIES.copy()

    if funding_source == "Workers' compensation":
        weights["Employer"] *= 3.0
        weights["Insurer or case manager"] *= 3.0
        weights["General practitioner"] *= 1.3
        weights["Self-referral"] *= 0.4

    if funding_source == "Compulsory third-party insurance":
        weights["Insurer or case manager"] *= 3.0
        weights["General practitioner"] *= 1.5
        weights["Self-referral"] *= 0.5

    if funding_source == "Medicare-supported care":
        weights["General practitioner"] *= 4.0
        weights["Self-referral"] *= 0.2

    if funding_source in {
        "Private health insurance",
        "Self-funded",
    }:
        weights["Self-referral"] *= 1.6

    referral_sources = list(weights.keys())
    probabilities = np.array(
        list(weights.values()),
        dtype=float,
    )

    probabilities = probabilities / probabilities.sum()

    return rng.choice(
        referral_sources,
        p=probabilities,
    )

# Generate referral sources conditionally
episodes_df["referral_source"] = [
    generate_referral_source(funding_source)
    for funding_source in episodes_df["funding_source"]
]

# Validate funding-source values
allowed_funding_sources = set(
    BASE_FUNDING_PROBABILITIES.keys()
)

invalid_funding_count = (
    ~episodes_df["funding_source"]
    .isin(allowed_funding_sources)
).sum()

# Validate referral-source values
allowed_referral_sources = set(
    BASE_REFERRAL_PROBABILITIES.keys()
)

invalid_referral_count = (
    ~episodes_df["referral_source"]
    .isin(allowed_referral_sources)
).sum()

print(
    "Invalid funding sources:",
    invalid_funding_count,
)

print(
    "Invalid referral sources:",
    invalid_referral_count,
)

# Compare referral sources across funding sources
print(
    pd.crosstab(
        episodes_df["funding_source"],
        episodes_df["referral_source"],
        normalize="index",
    )
    .round(2)
)

# Define the fixed data cutoff date
DATA_CUTOFF_DATE = pd.Timestamp("2026-09-28")

# Define episode-status probabilities
EPISODE_STATUS_VALUES = [
    "Completed",
    "Active",
    "Discontinued",
]

EPISODE_STATUS_PROBABILITIES = [
    0.65,
    0.25,
    0.10,
]

# Define episode-duration ranges
DURATION_RANGES = {
    "1-14 days": (1, 14),
    "15-42 days": (15, 42),
    "43-84 days": (43, 84),
    "85-168 days": (85, 168),
    "169-365 days": (169, 365),
}

DURATION_RANGE_PROBABILITIES = [
    0.10,
    0.30,
    0.35,
    0.20,
    0.05,
]

# Define discharge-reason probabilities
DISCHARGE_REASON_PROBABILITIES = {
    "Goals achieved": 0.55,
    "Patient discontinued": 0.15,
    "Referred to another provider": 0.10,
    "No further improvement": 0.08,
    "Lost to follow-up": 0.08,
    "Other": 0.04,
}

# Define the fixed data cutoff date
DATA_CUTOFF_DATE = pd.Timestamp("2026-09-28")

# Define episode-status probabilities
EPISODE_STATUS_VALUES = [
    "Completed",
    "Active",
    "Discontinued",
]

EPISODE_STATUS_PROBABILITIES = [
    0.65,
    0.25,
    0.10,
]

# Define episode-duration ranges
DURATION_RANGES = {
    "1-14 days": (1, 14),
    "15-42 days": (15, 42),
    "43-84 days": (43, 84),
    "85-168 days": (85, 168),
    "169-365 days": (169, 365),
}

DURATION_RANGE_PROBABILITIES = [
    0.10,
    0.30,
    0.35,
    0.20,
    0.05,
]

# Define discharge-reason probabilities
DISCHARGE_REASON_PROBABILITIES = {
    "Goals achieved": 0.55,
    "Patient discontinued": 0.15,
    "Referred to another provider": 0.10,
    "No further improvement": 0.08,
    "Lost to follow-up": 0.08,
    "Other": 0.04,
}

# Create a registration-date lookup by patient ID
registration_date_by_patient = (
    patients_df
    .set_index("patient_id")["registration_date"]
    .to_dict()
)

# Prepare episode date and status columns
episodes_df["episode_start_date"] = pd.NaT
episodes_df["episode_end_date"] = pd.NaT
episodes_df["episode_status"] = None
episodes_df["discharge_reason"] = None

# Generate non-overlapping episode dates for each patient
for patient_id, patient_episodes in episodes_df.groupby(
    "patient_id",
    sort=False,
):
    registration_date = registration_date_by_patient[
        patient_id
    ]

    episode_indexes = patient_episodes.index.tolist()
    episode_count = len(episode_indexes)

    available_days = (
        DATA_CUTOFF_DATE - registration_date
    ).days

    window_boundaries = np.linspace(
        0,
        available_days + 1,
        episode_count + 1,
        dtype=int,
    )

    for position, episode_index in enumerate(
        episode_indexes
    ):
        is_last_episode = (
            position == episode_count - 1
        )

        start_offset = window_boundaries[position]
        window_end_offset = (
            window_boundaries[position + 1] - 1
        )

        episode_start_date = (
            registration_date
            + pd.Timedelta(days=int(start_offset))
        )

        if is_last_episode:
            episode_status = rng.choice(
                EPISODE_STATUS_VALUES,
                p=EPISODE_STATUS_PROBABILITIES,
            )
        else:
            episode_status = rng.choice(
                ["Completed", "Discontinued"],
                p=[0.87, 0.13],
            )

        episodes_df.at[
            episode_index,
            "episode_start_date",
        ] = episode_start_date

        episodes_df.at[
            episode_index,
            "episode_status",
        ] = episode_status

        if episode_status == "Active":
            continue

        duration_group = rng.choice(
            list(DURATION_RANGES.keys()),
            p=DURATION_RANGE_PROBABILITIES,
        )

        minimum_duration, maximum_duration = (
            DURATION_RANGES[duration_group]
        )

        maximum_available_duration = max(
            1,
            window_end_offset - start_offset,
        )

        adjusted_minimum_duration = min(
            minimum_duration,
            maximum_available_duration,
        )

        adjusted_maximum_duration = min(
            maximum_duration,
            maximum_available_duration,
        )

        episode_duration = rng.integers(
            adjusted_minimum_duration,
            adjusted_maximum_duration + 1,
        )

        episode_end_date = (
            episode_start_date
            + pd.Timedelta(
                days=int(episode_duration)
            )
        )

        discharge_reason = rng.choice(
            list(
                DISCHARGE_REASON_PROBABILITIES.keys()
            ),
            p=list(
                DISCHARGE_REASON_PROBABILITIES.values()
            ),
        )

        episodes_df.at[
            episode_index,
            "episode_end_date",
        ] = episode_end_date

        episodes_df.at[
            episode_index,
            "discharge_reason",
        ] = discharge_reason

# Add registration dates temporarily for validation
validation_df = episodes_df.merge(
    patients_df[
        [
            "patient_id",
            "registration_date",
        ]
    ],
    on="patient_id",
    how="left",
)

# Validate episode start dates
invalid_start_date_count = (
    validation_df["episode_start_date"]
    < validation_df["registration_date"]
).sum()

# Validate episode end dates
ended_mask = validation_df[
    "episode_end_date"
].notna()

invalid_end_date_count = (
    validation_df.loc[
        ended_mask,
        "episode_end_date",
    ]
    < validation_df.loc[
        ended_mask,
        "episode_start_date",
    ]
).sum()

# Validate active episodes
active_mask = (
    validation_df["episode_status"] == "Active"
)

invalid_active_end_count = (
    validation_df.loc[
        active_mask,
        "episode_end_date",
    ]
    .notna()
    .sum()
)

invalid_active_discharge_count = (
    validation_df.loc[
        active_mask,
        "discharge_reason",
    ]
    .notna()
    .sum()
)

print(
    "Episodes starting before registration:",
    invalid_start_date_count,
)

print(
    "Episodes ending before they start:",
    invalid_end_date_count,
)

print(
    "Active episodes with an end date:",
    invalid_active_end_count,
)

print(
    "Active episodes with a discharge reason:",
    invalid_active_discharge_count,
)

# Define RTW status probabilities at episode start
RTW_START_PROBABILITIES = {
    "Full duties": 0.40,
    "Modified duties": 0.20,
    "Reduced hours": 0.15,
    "Not working": 0.25,
}


# Generate RTW status at episode start
def generate_rtw_status_at_start(
    occupation_group,
):
    if occupation_group == "Not currently employed":
        return "Not applicable"

    return rng.choice(
        list(RTW_START_PROBABILITIES.keys()),
        p=list(RTW_START_PROBABILITIES.values()),
    )


episodes_df["rtw_status_at_start"] = [
    generate_rtw_status_at_start(
        occupation_group
    )
    for occupation_group
    in episodes_df["occupation_group_at_start"]
]

# Define RTW transitions for completed episodes
COMPLETED_RTW_TRANSITIONS = {
    "Full duties": {
        "Full duties": 0.90,
        "Modified duties": 0.05,
        "Reduced hours": 0.03,
        "Not working": 0.02,
    },
    "Modified duties": {
        "Full duties": 0.55,
        "Modified duties": 0.30,
        "Reduced hours": 0.10,
        "Not working": 0.05,
    },
    "Reduced hours": {
        "Full duties": 0.45,
        "Modified duties": 0.25,
        "Reduced hours": 0.25,
        "Not working": 0.05,
    },
    "Not working": {
        "Full duties": 0.20,
        "Modified duties": 0.25,
        "Reduced hours": 0.20,
        "Not working": 0.35,
    },
}
# Define RTW transitions for discontinued episodes
DISCONTINUED_RTW_TRANSITIONS = {
    "Full duties": {
        "Full duties": 0.75,
        "Modified duties": 0.10,
        "Reduced hours": 0.08,
        "Not working": 0.07,
    },
    "Modified duties": {
        "Full duties": 0.15,
        "Modified duties": 0.45,
        "Reduced hours": 0.20,
        "Not working": 0.20,
    },
    "Reduced hours": {
        "Full duties": 0.10,
        "Modified duties": 0.20,
        "Reduced hours": 0.40,
        "Not working": 0.30,
    },
    "Not working": {
        "Full duties": 0.05,
        "Modified duties": 0.10,
        "Reduced hours": 0.15,
        "Not working": 0.70,
    },
}

# Generate RTW status at episode end
def generate_rtw_status_at_end(
    occupation_group,
    episode_status,
    rtw_status_at_start,
):
    if episode_status == "Active":
        return None

    if occupation_group == "Not currently employed":
        return "Not applicable"

    if episode_status == "Completed":
        transition_probabilities = (
            COMPLETED_RTW_TRANSITIONS[
                rtw_status_at_start
            ]
        )
    else:
        transition_probabilities = (
            DISCONTINUED_RTW_TRANSITIONS[
                rtw_status_at_start
            ]
        )

    return rng.choice(
        list(transition_probabilities.keys()),
        p=list(transition_probabilities.values()),
    )

# Generate RTW status at episode end
episodes_df["rtw_status_at_end"] = [
    generate_rtw_status_at_end(
        occupation_group,
        episode_status,
        rtw_status_at_start,
    )
    for (
        occupation_group,
        episode_status,
        rtw_status_at_start,
    ) in zip(
        episodes_df["occupation_group_at_start"],
        episodes_df["episode_status"],
        episodes_df["rtw_status_at_start"],
    )
]

# Define validation masks
unemployed_mask = (
    episodes_df["occupation_group_at_start"]
    == "Not currently employed"
)

employed_mask = ~unemployed_mask

active_mask = (
    episodes_df["episode_status"] == "Active"
)

closed_mask = ~active_mask

# Validate RTW status at episode start
invalid_unemployed_start_count = (
    episodes_df.loc[
        unemployed_mask,
        "rtw_status_at_start",
    ]
    .ne("Not applicable")
    .sum()
)

invalid_employed_start_count = (
    episodes_df.loc[
        employed_mask,
        "rtw_status_at_start",
    ]
    .eq("Not applicable")
    .sum()
)

# Validate RTW status at episode end
invalid_active_end_count = (
    episodes_df.loc[
        active_mask,
        "rtw_status_at_end",
    ]
    .notna()
    .sum()
)

invalid_unemployed_closed_end_count = (
    episodes_df.loc[
        unemployed_mask & closed_mask,
        "rtw_status_at_end",
    ]
    .ne("Not applicable")
    .sum()
)

print(
    "Invalid unemployed RTW start values:",
    invalid_unemployed_start_count,
)

print(
    "Invalid employed RTW start values:",
    invalid_employed_start_count,
)

print(
    "Active episodes with RTW end values:",
    invalid_active_end_count,
)

print(
    "Invalid unemployed closed RTW end values:",
    invalid_unemployed_closed_end_count,
)

# Sort episodes before checking for overlapping periods
ordered_episodes_df = episodes_df.sort_values(
    [
        "patient_id",
        "episode_start_date",
    ]
)

# Retrieve the previous episode end date
previous_end_dates = (
    ordered_episodes_df
    .groupby("patient_id")["episode_end_date"]
    .shift(1)
)

# Count overlapping episode periods
overlapping_episode_count = (
    previous_end_dates.notna()
    & (
        ordered_episodes_df["episode_start_date"]
        <= previous_end_dates
    )
).sum()

print(
    "Overlapping episode periods:",
    overlapping_episode_count,
)

# Validate primary and foreign keys
duplicate_episode_id_count = (
    episodes_df["episode_id"]
    .duplicated()
    .sum()
)

invalid_patient_reference_count = (
    ~episodes_df["patient_id"]
    .isin(patients_df["patient_id"])
).sum()

# Validate active episode fields
active_mask = (
    episodes_df["episode_status"] == "Active"
)

invalid_active_end_date_count = (
    episodes_df.loc[
        active_mask,
        "episode_end_date",
    ]
    .notna()
    .sum()
)

invalid_active_discharge_count = (
    episodes_df.loc[
        active_mask,
        "discharge_reason",
    ]
    .notna()
    .sum()
)

# Validate closed episode fields
closed_mask = ~active_mask

invalid_closed_end_date_count = (
    episodes_df.loc[
        closed_mask,
        "episode_end_date",
    ]
    .isna()
    .sum()
)

invalid_closed_discharge_count = (
    episodes_df.loc[
        closed_mask,
        "discharge_reason",
    ]
    .isna()
    .sum()
)

print(
    "Duplicate episode IDs:",
    duplicate_episode_id_count,
)

print(
    "Invalid patient references:",
    invalid_patient_reference_count,
)

print(
    "Active episodes with an end date:",
    invalid_active_end_date_count,
)

print(
    "Active episodes with a discharge reason:",
    invalid_active_discharge_count,
)

print(
    "Closed episodes without an end date:",
    invalid_closed_end_date_count,
)

print(
    "Closed episodes without a discharge reason:",
    invalid_closed_discharge_count,
)

# Define the final episode-column order
EPISODE_COLUMNS = [
    "episode_id",
    "patient_id",
    "condition_group",
    "primary_body_region",
    "injury_mechanism",
    "occupation_group_at_start",
    "physical_work_demand_at_start",
    "referral_source",
    "funding_source",
    "episode_start_date",
    "episode_end_date",
    "episode_status",
    "rtw_status_at_start",
    "rtw_status_at_end",
    "discharge_reason",
]

# Apply the final column order
episodes_df = episodes_df[EPISODE_COLUMNS]

# Save the synthetic episode data
episodes_df.to_csv(
    EPISODES_PATH,
    index=False,
    date_format="%Y-%m-%d",
)

print(
    f"episodes.csv saved successfully: {EPISODES_PATH}"
)

print(
    "Final episode shape:",
    episodes_df.shape,
)

print(
    episodes_df.head()
)

