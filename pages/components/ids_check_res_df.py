"""Module for IDS check results evaluation"""

import pandas as pd
from loguru import logger


def create_specifications_dataframe(data: dict):
    # Initialize counters
    total_checks = 0
    passed_checks = 0
    failed_checks = 0

    rows = []

    # Iterate through specifications
    for spec in data["specifications"]:
        # For each requirement, we only need the description
        for req in spec["requirements"]:
            row = {
                "Specification Name": spec["name"],
                "Requirement": req["description"],
                "Total Checks": req["total_applicable"],
                "Passed Checks": req["total_pass"],
                "Failed Checks": req["total_fail"],
            }
            rows.append(row)

            # Aggregate total and passed checks
            total_checks += req["total_applicable"]
            passed_checks += req["total_pass"]

            # Calculate failed checks
            failed_checks += req["total_fail"]

            logger.info(f"Spec total checks per requirement {spec['total_checks']}")
            logger.info(f"Total checks {total_checks}")

    # Create DataFrame
    df = pd.DataFrame(rows)

    def _calc_passed_percentage(row_) -> str | None:
        """Calculate the total passed checks percentage of a specification"""
        # Check for zero total checks to avoid division by zero
        if row_["Total Checks"] == 0:
            return None
        else:
            # Calculate the percentage
            percentage = (row_["Passed Checks"] / row_["Total Checks"]) * 100
            # Return the percentage with three decimal places
            return f"{percentage:.2f}"

    # Apply the function to calculate 'Passed Percentage'
    df["Passed Percentage"] = df.apply(_calc_passed_percentage, axis=1)

    # Add summary row
    summary_row = {
        "Specification Name": "Total/Average",
        "Requirement": "N/A",
        "Total Checks": total_checks,
        "Passed Checks": passed_checks,
        "Failed Checks": failed_checks,
        "Passed Percentage": f"{(passed_checks / total_checks * 100):.2f}" if total_checks > 0 else "0.00",
    }

    df = df.append(summary_row, ignore_index=True)

    # Define a function to apply colors
    def color_pass_fail(val: str | None) -> str:
        if pd.isnull(val):  # check for NaN or None
            return "background-color: gray"

        else:  # apply only to numeric columns
            val = float(val)
            if val < 30:  # assuming a fail if less than 50% pass
                return "background-color: red"
            if val < 50:  # assuming a fail if less than 50% pass
                return "background-color: orange"
            elif val < 70:  # assuming a fail if less than 50% pass
                return "background-color: yellow"
            elif val >= 70:
                return "background-color: green"

        return ""  # return empty string for other types

    # Apply color styling to the DataFrame
    styled_df = df.style.applymap(color_pass_fail, subset=["Passed Percentage"])

    return styled_df
