# CSV Schema Filter

> **A lightweight, schema-driven CSV validation and filtering utility built with Python, Pandas, and NumPy.**

CSV files are easy to create, but downstream data pipelines often assume that incoming data follows a specific structure. A renamed column, missing field, unexpected field, or incompatible data type can silently break later processing.

**CSV Schema Filter** provides a small, reusable solution to this problem.

It treats the expected dataset structure as a **schema contract**, validates an incoming CSV against that contract, detects structural and data-type mismatches, and produces a filtered dataset together with a machine-readable validation report.

---

## Why This Project?

In a typical data pipeline:

```text
Source System
     ↓
CSV File
     ↓
Data Validation
     ↓
Transformation
     ↓
Data Warehouse
     ↓
Analytics
```

The CSV entering the pipeline cannot always be assumed to have the expected structure.

For example:

```text
Expected:
Order_ID
Product_Name
Units_Sold
Revenue
Profit

Incoming:
Order_ID
Product_Name
Units_Sold
Revenue
Customer_Segment
```

The dataset has changed.

Instead of allowing this change to pass unnoticed, CSV Schema Filter identifies:

```text
Missing:
Profit

Unexpected:
Customer_Segment
```

This makes schema problems visible **before the dataset moves further downstream**.

---

## What Does It Do?

CSV Schema Filter performs four main operations:

### 1. Schema Comparison

Compares the incoming CSV columns against a predefined schema.

It identifies:

* Present columns
* Missing columns
* Unexpected columns

### 2. Data-Type Validation

Checks whether each expected column has the data type defined by the schema.

For example:

```text
Expected: datetime
Actual:   object
Result:   INVALID
```

### 3. Schema-Based Filtering

Creates a new DataFrame containing only columns defined by the schema.

Unexpected columns are excluded from the filtered output.

### 4. Validation Reporting

Generates a structured JSON report containing:

* Input dataset size
* Expected schema size
* Present columns
* Missing columns
* Unexpected columns
* Type validation results
* Output dataset size

---

## Architecture

```text
                    ┌─────────────────────┐
                    │    Incoming CSV     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Schema Contract  │
                    │      schema.py      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Schema Validator  │
                    │     validator.py    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             Column Validation       Type Validation
                    │                     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Schema Filtering  │
                    │      filter.py      │
                    └──────────┬──────────┘
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
              Filtered CSV         JSON Report
```

---

## Project Structure

```text
csv-schema-filter/
│
├── data/
│   ├── raw/
│   │   └── Nike_Sales_Uncleaned.csv
│   │
│   └── test/
│       └── schema_drift.csv
│
├── src/
│   ├── schema.py
│   ├── validator.py
│   ├── filter.py
│   └── report.py
│
├── output/
│   ├── nike_filtered.csv
│   └── validation_report.json
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

> Dataset files may be excluded from the Git repository depending on their source and redistribution terms.

---

## Schema Contract

The expected structure is defined separately from the processing logic.

Example:

```python
SCHEMA = {
    "Order_ID": {
        "type": "integer",
        "required": True
    },
    "Gender_Category": {
        "type": "string",
        "required": True
    },
    "Product_Line": {
        "type": "string",
        "required": True
    },
    "Revenue": {
        "type": "float",
        "required": True
    },
    "Order_Date": {
        "type": "datetime",
        "required": True
    }
}
```

This separation is intentional.

The validation engine does not need to know anything specific about the Nike dataset. The expected structure is provided through the schema configuration.

That makes the validation logic reusable for other CSV datasets.

---

## Validation Flow

The project processes an incoming dataset in this order:

```text
Load CSV
   ↓
Compare Columns
   ↓
Validate Data Types
   ↓
Filter According to Schema
   ↓
Generate Validation Report
   ↓
Save Outputs
```

The result is two important artifacts:

```text
nike_filtered.csv
validation_report.json
```

---

## Schema Drift Detection

One of the project's main features is detecting structural changes in an incoming dataset.

For example, suppose the schema expects:

```text
Profit
```

but the incoming dataset does not contain it.

At the same time, the source adds:

```text
Customer_Segment
```

The validator reports:

```json
{
    "columns": {
        "present": 10,
        "missing": 1,
        "unexpected": 3,
        "unexpected_columns": [
            "Customer_Segement",
            "Discount_Applied",
            "Size"
        ]
    }
}
```

This demonstrates how the utility can expose changes in an incoming dataset instead of silently passing them downstream.

---

## Example Validation Report

A generated report has the following structure:

```json
{
    "input": {
        "rows": 2500,
        "columns": 13
    },
    "schema": {
        "expected_columns": 11
    },
    "columns": {
        "present": 10,
        "missing": 1,
        "unexpected": 3,
        "unexpected_columns": [
            "Customer_Segement",
            "Discount_Applied",
            "Size"
        ]
    },
    "types": {
        "valid": 9,
        "mismatches": 1
    },
    "output": {
        "rows": 2500,
        "columns": 10
    }
}
```

The report provides a compact machine-readable summary of the validation process.

---

## Technology Stack

| Technology | Purpose                                                     |
| ---------- | ----------------------------------------------------------- |
| **Python** | Application logic and orchestration                         |
| **Pandas** | CSV loading, DataFrame processing, filtering and inspection |
| **NumPy**  | Data-type family validation                                 |
| **JSON**   | Machine-readable validation reporting                       |

---

## Why Pandas and NumPy?

### Pandas

Pandas is responsible for the dataset-level operations:

* Reading CSV files
* Inspecting columns
* Accessing dtypes
* Filtering columns
* Creating the output dataset

### NumPy

NumPy is used specifically for dtype-family validation.

For example:

```python
np.issubdtype(actual_dtype, np.integer)
```

This allows the validator to check whether a column belongs to the expected numeric type family rather than relying only on string comparisons.

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd csv-schema-filter
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Place the input CSV inside:

```text
data/raw/
```

Update the input path in `main.py` if necessary:

```python
df = pd.read_csv("data/Nike_Sales_Uncleaned.csv")
```

Then run:

```bash
python main.py
```

The program will:

1. Load the dataset
2. Compare columns against the schema
3. Validate data types
4. Filter the dataset
5. Save the filtered CSV
6. Generate the JSON validation report

---

## Output

After execution:

```text
output/
├── nike_filtered.csv
└── validation_report.json
```

### Filtered CSV

Contains only the columns defined by the schema.

### Validation Report

Contains a structured summary of the validation results.

---

## Real-World Data Scenario

The project uses an uncleaned Nike sales dataset containing characteristics commonly encountered in real datasets, including:

* Missing values
* Numeric fields with missing entries
* Date values represented as strings
* Multiple categorical fields
* Additional columns outside the target schema

The project intentionally **does not perform general data cleaning**.

Its responsibility is narrower:

> **Determine whether the structure of the incoming dataset matches the expected schema and produce a schema-compliant column set.**

This separation keeps validation and cleaning as distinct pipeline responsibilities.

---

## Design Principle

The project follows a simple principle:

```text
Don't assume the input schema.
Validate it.
```

Instead of embedding expected column names and types throughout the application, the schema is maintained separately.

```text
Schema
  +
Validator
  +
Filter
  +
Report
```

This separation makes the project easier to understand, modify, and extend.

---

## Limitations

This project intentionally keeps the implementation lightweight.

Current limitations include:

* Basic dtype validation
* No automatic data type conversion
* No missing-value imputation
* No duplicate-data handling
* No database integration
* No streaming validation
* No distributed processing

These are outside the current scope because the project's primary purpose is **schema validation and filtering**.

---

## Possible Future Extensions

The architecture can be extended with features such as:

```text
Schema Versioning
       ↓
Strict / Lenient Validation Modes
       ↓
Schema Fingerprinting
       ↓
Data Quality Rules
       ↓
Pipeline Integration
       ↓
Database / BigQuery Validation
```

Potential future capabilities could include:

* Configurable schemas using YAML or JSON
* Schema version comparison
* Row-level validation rules
* Nullability rules
* Numeric range validation
* Automated validation summaries
* BigQuery integration
* CI/CD validation
* Pipeline failure thresholds

---

## Project Goal

This project was built to explore how a relatively small Python utility can solve a practical data-engineering problem:

**How can an incoming CSV dataset be checked against an expected contract before downstream processing?**

Rather than focusing only on DataFrame manipulation, the project separates:

```text
Configuration
     ↓
Validation
     ↓
Filtering
     ↓
Reporting
```

This makes the project a compact demonstration of **schema-driven data processing using Python, Pandas, and NumPy**.

---

## License

This project is intended for learning and portfolio purposes.

If a third-party dataset is included, its original licensing and usage terms should be followed.
