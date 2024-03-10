"""Модуль для обработки кузультатов IDS проверки"""
import pandas as pd


def create_specifications_dataframe(data: dict):
    # Initialize counters
    total_checks = 0
    passed_checks = 0
    failed_checks = 0

    rows = []

    # Iterate through specifications
    for spec in data['specifications']:
        # Aggregate total and passed checks
        total_checks += spec['total_checks']
        passed_checks += spec['total_checks_pass']

        # Calculate failed checks
        failed_checks += spec['total_checks'] - spec['total_checks_pass']

        # For each requirement, we only need the description
        for req in spec['requirements']:
            row = {
                'Specification Name': spec['name'],
                'Requirement': req['description'],
                'Total Checks': spec['total_checks'],
                'Passed Checks': spec['total_checks_pass'],
                'Failed Checks': spec['total_checks'] - spec['total_checks_pass']
            }
            rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows)

    # Calculate percentages and add as a new column
    try:
        df['Passed Percentage'] = ((df['Passed Checks'] / df['Total Checks']) * 100).round().astype(int)

    except Exception:
        df['Passed Percentage'] = (df['Passed Checks'] / df['Total Checks']) * 100

    # Add summary row
    summary_row = {
        'Specification Name': 'Total/Average',
        'Requirement': 'N/A',
        'Total Checks': total_checks,
        'Passed Checks': passed_checks,
        'Failed Checks': failed_checks,
        'Passed Percentage': round((passed_checks / total_checks * 100)) if total_checks > 0 else 0
    }

    df = df.append(summary_row, ignore_index=True)

    # Define a function to apply colors
    def color_pass_fail(val):
        if isinstance(val, (float, int)):  # apply only to numeric columns
            if val < 50:  # assuming a fail if less than 50% pass
                return 'background-color: red'
            elif val < 80:  # assuming a fail if less than 50% pass
                return 'background-color: yellow'
            else:
                return 'background-color: green'
        return ''  # return empty string for other types

    # Apply color styling to the DataFrame
    styled_df = df.style.applymap(color_pass_fail, subset=['Passed Percentage'])

    return styled_df
