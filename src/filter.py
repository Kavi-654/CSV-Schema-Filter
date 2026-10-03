from src.schema import SCHEMA


def filter_by_schema(df):
    expected_columns = list(SCHEMA.keys())

    available_columns = [
        column
        for column in expected_columns
        if column in df.columns
    ]

    filtered_df = df[available_columns].copy()

    return filtered_df