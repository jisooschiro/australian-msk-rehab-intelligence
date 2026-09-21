import numpy as np
import pandas as pd


RANDOM_SEED = 42
PATIENT_COUNT = 1_000

rng = np.random.default_rng(RANDOM_SEED)

# 연령대별 생성 확률
AGE_GROUP_PROBABILITIES = {
    "18-24": 0.08,
    "25-34": 0.18,
    "35-44": 0.22,
    "45-54": 0.24,
    "55-64": 0.18,
    "65-74": 0.08,
    "75-85": 0.02,
}

# 각 연령대의 최소·최대 나이
AGE_RANGES = {
    "18-24": (18, 24),
    "25-34": (25, 34),
    "35-44": (35, 44),
    "45-54": (45, 54),
    "55-64": (55, 64),
    "65-74": (65, 74),
    "75-85": (75, 85),
}

age_groups = rng.choice(
    list(AGE_GROUP_PROBABILITIES.keys()),
    size=PATIENT_COUNT,
    p=list(AGE_GROUP_PROBABILITIES.values()),
)

ages_at_registration = []

for age_group in age_groups:
    min_age, max_age = AGE_RANGES[age_group]

    age = rng.integers(
        low=min_age,
        high=max_age + 1,
    )

    ages_at_registration.append(age)

ages_at_registration = np.array(ages_at_registration)

registration_dates = pd.to_datetime(
    rng.choice(
        pd.date_range(
            start="2024-01-01",
            end="2026-08-31",
            freq="D",
        ),
        size=PATIENT_COUNT,
    )
)

years_of_birth = (
    registration_dates.year
    - ages_at_registration
)

test_df = pd.DataFrame({
    "age_group": age_groups,
    "age_at_registration": ages_at_registration,
    "registration_date": registration_dates,
    "year_of_birth": years_of_birth,
})

print(test_df.head())

print(
    test_df["age_group"]
    .value_counts(normalize=True)
    .sort_index()
)

print(
    test_df["age_at_registration"]
    .agg(["min", "max"])
)

# Define recorded sex probabilities
SEX_PROBABILITIES = {
    "Female": 0.50,
    "Male": 0.48,
    "Intersex": 0.005,
    "Other": 0.005,
    "Not stated": 0.01,
}

# Generate recorded sex values
sex_values = rng.choice(
    list(SEX_PROBABILITIES.keys()),
    size=PATIENT_COUNT,
    p=list(SEX_PROBABILITIES.values()),
)

# Generate unique patient identifiers
patient_ids = [
    f"P{i:04d}"
    for i in range(1, PATIENT_COUNT + 1)
]

# Preview the first and last patient identifiers
print(patient_ids[:5])
print(patient_ids[-5:])

# Create the final patient DataFrame
patients_df = pd.DataFrame({
    "patient_id": patient_ids,
    "year_of_birth": years_of_birth,
    "sex": sex_values,
    "registration_date": registration_dates,
})

# Preview the generated patient data
patients_df.head()

# Recalculate age at registration for validation
calculated_ages = (
    patients_df["registration_date"].dt.year
    - patients_df["year_of_birth"]
)

# Define the permitted recorded sex values
allowed_sex_values = set(SEX_PROBABILITIES.keys())

# Run validation checks
print("Number of rows:", len(patients_df))
print("Duplicate patient IDs:", patients_df["patient_id"].duplicated().sum())
print("Total missing values:", patients_df.isna().sum().sum())
print("Minimum age:", calculated_ages.min())
print("Maximum age:", calculated_ages.max())
print(
    "Invalid sex values:",
    (~patients_df["sex"].isin(allowed_sex_values)).sum()
)

