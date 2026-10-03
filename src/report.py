def generate_report(df, column_result, type_result, filtered_df):

    valid_types = sum(
        result["valid"]
        for result in type_result.values()
    )

    type_mismatches = len(type_result) - valid_types

    report = {
        "input": {
            "rows": len(df),
            "columns": len(df.columns)
        },

        "schema": {
            "expected_columns": len(
                column_result["present"]
            ) + len(
                column_result["missing"]
            )
        },

        "columns": {
            "present": len(column_result["present"]),
            "missing": len(column_result["missing"]),
            "unexpected": len(column_result["unexpected"]),
            "unexpected_columns": column_result["unexpected"]
        },

        "types": {
            "valid": valid_types,
            "mismatches": type_mismatches
        },

        "output": {
            "rows": len(filtered_df),
            "columns": len(filtered_df.columns)
        }
    }

    return report