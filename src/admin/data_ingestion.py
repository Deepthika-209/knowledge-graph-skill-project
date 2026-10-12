import io
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


DATASET_SCHEMAS = {
    "Domains": {
        "filename": "domains.csv",
        "required": ["name", "description", "parent_domain"],
    },
    "Skills": {
        "filename": "skills.csv",
        "required": [

            "name",
            "type",
             "difficulty",
            "description",
            "is_technology"
        ],
    },
    "Skill Domains": {
        "filename": "skill_domains.csv",
        "required": ["skill", "domain"],
    },
    "Skill Prerequisites": {
        "filename": "skill_prerequisites.csv",
        "required": ["skill", "prerequisite"],
    },
    "Skill Related": {
        "filename": "skill_related.csv",
        "required": ["skill", "related_skill"],
    },
    "Projects": {
        "filename": "projects.csv",
        "required": ["project", "domain", "level"],
    },
    "Project Skills": {
        "filename": "project_skills.csv",
        "required": ["project", "skill", "relevance"],
    },
    "Courses": {
        "filename": "courses.csv",
        "required": [
            "course_id",
            "title",
            "platform",
            "domain",
            "level",
            "duration_hours",
            "url",
        ],
    },
    "Course Skills": {
        "filename": "course_skills.csv",
        "required": ["course", "skill", "relevance"],
    },
    "Internships": {
        "filename": "internships.csv",
        "required": [
            "internship_id",
            "title",
            "company",
            "domain",
            "level",
            "duration_months",
            "location",
            "mode",
            "url",
        ],
    },
    "Internship Skills": {
        "filename": "internship_skills.csv",
        "required": ["internship", "skill", "relevance"],
    },
}


def get_dataset_types():
    """Return all supported dataset types."""
    return list(DATASET_SCHEMAS.keys())


def read_uploaded_file(uploaded_file):
    """
    Read CSV or Excel uploaded through Streamlit.
    Returns a pandas DataFrame.
    """

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if file_name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    if file_name.endswith(".xls"):
        return pd.read_excel(uploaded_file)

    raise ValueError(
        "Unsupported file format. Please upload CSV or Excel (.xlsx/.xls)."
    )


def validate_dataframe(dataframe, dataset_type):
    """
    Validate uploaded data against the expected schema.
    """

    if dataset_type not in DATASET_SCHEMAS:
        return False, ["Unknown dataset type."]

    required_columns = DATASET_SCHEMAS[dataset_type]["required"]

    uploaded_columns = list(dataframe.columns)

    missing_columns = [
        column
        for column in required_columns
        if column not in uploaded_columns
    ]

    if missing_columns:
        return False, [
            "Missing required column(s): "
            + ", ".join(missing_columns)
        ]

    if dataframe.empty:
        return False, ["The uploaded file contains no records."]

    errors = []

    # Check required columns for empty values.
    for column in required_columns:
        empty_count = dataframe[column].isna().sum()

        if empty_count > 0:
            errors.append(
                f"Column '{column}' contains "
                f"{empty_count} empty value(s)."
            )

    # Check duplicate rows.
    duplicate_count = dataframe.duplicated().sum()

    if duplicate_count > 0:
        errors.append(
            f"The file contains {duplicate_count} duplicate row(s)."
        )

    # Numeric validation.
    if dataset_type == "Skills":
        if "difficulty" in dataframe.columns:
            invalid = pd.to_numeric(
                dataframe["difficulty"],
                errors="coerce"
            ).isna().sum()

            if invalid > 0:
                errors.append(
                    "The 'difficulty' column contains "
                    "non-numeric value(s)."
                )

    if dataset_type == "Projects":
        if "level" not in dataframe.columns:
            errors.append("Project level is required.")

    if dataset_type == "Project Skills":
        if "relevance" in dataframe.columns:
            invalid = pd.to_numeric(
                dataframe["relevance"],
                errors="coerce"
            ).isna().sum()

            if invalid > 0:
                errors.append(
                    "The 'relevance' column contains "
                    "non-numeric value(s)."
                )

    if dataset_type == "Course Skills":
        if "relevance" in dataframe.columns:
            invalid = pd.to_numeric(
                dataframe["relevance"],
                errors="coerce"
            ).isna().sum()

            if invalid > 0:
                errors.append(
                    "The 'relevance' column contains "
                    "non-numeric value(s)."
                )

    if dataset_type == "Internship Skills":
        if "relevance" in dataframe.columns:
            invalid = pd.to_numeric(
                dataframe["relevance"],
                errors="coerce"
            ).isna().sum()

            if invalid > 0:
                errors.append(
                    "The 'relevance' column contains "
                    "non-numeric value(s)."
                )

    # We allow duplicate warnings but block structural errors.
    blocking_errors = [
        error
        for error in errors
        if "duplicate" not in error.lower()
    ]

    if blocking_errors:
        return False, errors

    return True, errors


def save_dataframe(dataframe, dataset_type):
    """
    Save validated dataframe into the project's data directory.
    """

    if dataset_type not in DATASET_SCHEMAS:
        raise ValueError("Unknown dataset type.")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    filename = DATASET_SCHEMAS[dataset_type]["filename"]
    output_path = DATA_DIR / filename

    dataframe.to_csv(
        output_path,
        index=False,
        encoding="utf-8"
    )

    return output_path


def import_dataset(uploaded_file, dataset_type):
    """
    Complete ingestion pipeline:
    read → validate → save.
    """

    try:
        dataframe = read_uploaded_file(uploaded_file)
    except Exception as error:
        return {
            "success": False,
            "message": f"Could not read file: {error}",
            "rows": 0,
            "warnings": [],
        }

    valid, messages = validate_dataframe(
        dataframe,
        dataset_type
    )

    if not valid:
        return {
            "success": False,
            "message": "Dataset validation failed.",
            "rows": len(dataframe),
            "warnings": messages,
        }

    try:
        output_path = save_dataframe(
            dataframe,
            dataset_type
        )

        return {
            "success": True,
            "message": (
                f"{dataset_type} imported successfully."
            ),
            "rows": len(dataframe),
            "warnings": messages,
            "path": str(output_path),
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Could not save dataset: {error}",
            "rows": len(dataframe),
            "warnings": messages,
        }


def get_dataset_status():
    """
    Return row counts and existence status
    for every supported dataset.
    """

    status = []

    for dataset_type, config in DATASET_SCHEMAS.items():

        file_path = DATA_DIR / config["filename"]

        if not file_path.exists():
            status.append({
                "dataset": dataset_type,
                "file": config["filename"],
                "exists": False,
                "rows": 0,
            })
            continue

        try:
            dataframe = pd.read_csv(file_path)

            status.append({
                "dataset": dataset_type,
                "file": config["filename"],
                "exists": True,
                "rows": len(dataframe),
            })

        except Exception:
            status.append({
                "dataset": dataset_type,
                "file": config["filename"],
                "exists": True,
                "rows": 0,
            })

    return status


if __name__ == "__main__":

    print("=" * 60)
    print("DATA INGESTION MODULE TEST")
    print("=" * 60)

    print("\nSupported datasets:")

    for dataset in get_dataset_types():
        print(f"  - {dataset}")

    print("\nCurrent dataset status:")

    for item in get_dataset_status():
        status = "AVAILABLE" if item["exists"] else "MISSING"

        print(
            f"  {item['dataset']}: "
            f"{status} | "
            f"{item['rows']} row(s)"
        )

    print("\n" + "=" * 60)