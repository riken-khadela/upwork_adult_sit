from datetime import datetime, timedelta
import re

def naughty_convert_relative_time(relative_time):
    # Define regular expression pattern to extract numerical value and time unit
    pattern = r'(\d+)\s+(\w+)'

    # Match the pattern in the relative_time string
    match = re.match(pattern, relative_time)

    if match:
        # Extract numerical value and time unit
        value = int(match.group(1))
        unit = match.group(2).lower()

        # Map time units to timedelta arguments
        unit_mapping = {
            'year': 'years',
            'month': 'months',
            'week': 'weeks',
            'day': 'days'
        }

        # Calculate the date based on the provided relative time
        date = datetime.now() - timedelta(**{unit_mapping.get(unit, 'days'): value})

        # Format the date as "Sep 1, 2023"
        formatted_date = date.strftime("%b %d, %Y")

        return formatted_date
