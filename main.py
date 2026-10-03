import json
import pandas as pd

from src.validator import compare_columns, validate_types
from src.filter import filter_by_schema
from src.report import generate_report


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv("data/Nike_Sales_Uncleaned.csv")


# --------------------------------------------------
# 2. Compare dataset columns with expected schema
# --------------------------------------------------

column_result = compare_columns(df)

print("Present columns:")
print(column_result["present"])

print("\nMissing columns:")
print(column_result["missing"])

print("\nUnexpected columns:")
print(column_result["unexpected"])


# --------------------------------------------------
# 3. Validate data types
# --------------------------------------------------

type_result = validate_types(df)

print("\nType Validation:")

for column, result in type_result.items():
    print(
        f"{column}: "
        f"expected={result['expected']}, "
        f"actual={result['actual']}, "
        f"valid={result['valid']}"
    )


# --------------------------------------------------
# 4. Filter dataset according to schema
# --------------------------------------------------

filtered_df = filter_by_schema(df)


# --------------------------------------------------
# 5. Save filtered dataset
# --------------------------------------------------

output_path = "output/nike_filtered.csv"

filtered_df.to_csv(
    output_path,
    index=False
)

print("\nOriginal shape:", df.shape)
print("Filtered shape:", filtered_df.shape)
print("Saved to:", output_path)


# --------------------------------------------------
# 6. Generate validation report
# --------------------------------------------------

report = generate_report(
    df,
    column_result,
    type_result,
    filtered_df
)


# --------------------------------------------------
# 7. Save validation report as JSON
# --------------------------------------------------

report_path = "output/validation_report.json"

with open(report_path, "w") as file:
    json.dump(report, file, indent=4)

print("Validation report saved to:", report_path)
