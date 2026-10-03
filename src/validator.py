from src.schema import SCHEMA
import numpy as np


def compare_columns(df):
    expected_columns = set(SCHEMA.keys())
    actual_columns = set(df.columns)

    present_columns = expected_columns.intersection(actual_columns)
    missing_columns = expected_columns.difference(actual_columns)
    unexpected_columns = actual_columns.difference(expected_columns)

    return {
        "present": sorted(present_columns),
        "missing": sorted(missing_columns),
        "unexpected": sorted(unexpected_columns)
    }

def validate_types(df):
        type_results = {}

        for column, rules in SCHEMA.items():

            if column not in df.columns:
                continue

            actual_dtype = df[column].dtype
            expected_type = rules["type"]

            if expected_type == "integer":
                is_valid = np.issubdtype(actual_dtype, np.integer)

            elif expected_type == "float":
                is_valid = np.issubdtype(actual_dtype, np.floating)

            elif expected_type == "string":
                is_valid = df[column].dtype == "object"

            elif expected_type == "datetime":
                is_valid = np.issubdtype(actual_dtype, np.datetime64)

            else:
                is_valid = False

            type_results[column] = {
                "expected": expected_type,
                "actual": str(actual_dtype),
                "valid": is_valid
            }

        return type_results
