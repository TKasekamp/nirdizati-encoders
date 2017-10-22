from datetime import datetime as dt

import numpy as np
import pandas as pd

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_COLUMNS = ["case_id", "event_nr", "remaining_time", "elapsed_time"]


def get_events(df):
    return df['activity_name'].unique()


def get_cases(df):
    return df['case_id'].unique()


def calculate_remaining_time(trace, event_nr):
    event_timestamp = trace[trace["event_nr"] == event_nr]['time'].apply(str).item()
    event_timestamp = dt.strptime(event_timestamp, TIME_FORMAT)
    last_event_timestamp = trace[trace["event_nr"] == len(trace)]['time'].apply(str).item()
    last_event_timestamp = dt.strptime(last_event_timestamp, TIME_FORMAT)
    return (last_event_timestamp - event_timestamp).total_seconds()


def calculate_elapsed_time(trace, event_nr):
    event_timestamp = trace[trace["event_nr"] == event_nr]['time'].apply(str).item()
    event_timestamp = dt.strptime(event_timestamp, TIME_FORMAT)
    first_event_timestamp = trace[trace["event_nr"] == 1]['time'].apply(str).item()
    first_event_timestamp = dt.strptime(first_event_timestamp, TIME_FORMAT)
    return (event_timestamp - first_event_timestamp).total_seconds()


def encode_boolean_frequency(data, encoding):
    """Internal method for both boolean and frequency. Only dif is __append_item"""
    events = get_events(data)
    cases = get_cases(data)

    columns = np.append(events, list(DEFAULT_COLUMNS))
    encoded_data = pd.DataFrame(columns=columns)

    i = 0
    for case in cases:
        df = data[data['case_id'] == case]
        for j in range(0, max(df['event_nr'])):
            case_data = []
            event_length = j + 1
            for event in events:
                case_data.append(__append_item(df, event, event_length, encoding))
            case_data.append(case)
            case_data.append(event_length)
            remaining_time = calculate_remaining_time(df, event_length)
            case_data.append(remaining_time)
            elapsed_time = calculate_elapsed_time(df, event_length)
            case_data.append(elapsed_time)
            encoded_data.loc[i] = case_data
            i = i + 1

    return encoded_data


def __append_item(df, event, event_length, encoding):
    """Boolean returns if len is > 0, frequency returns len"""
    length = len(df[(df['activity_name'] == event) & (df['event_nr'] <= event_length)])
    if encoding == 'boolean':
        return length > 0
    elif encoding == 'frequency':
        return length
