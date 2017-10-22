from nirdizati.encoders.helper import *

import numpy as np
import pandas as pd


def encode_boolean_frequency(data, encoding='boolean'):
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


def encode_complex_index_latest(data, additional_columns, prefix_length=1, encoding='complex'):
    """Internal method for complex and index latest encoding.
        Diff in columns and case_data.
    """
    cases = get_cases(data)
    columns = __create_columns(prefix_length, additional_columns, encoding)
    encoded_data = []

    for case in cases:
        df = data[data['case_id'] == case]
        event_length = prefix_length
        # uncomment to encode whole log at each prefix
        # for event_length in range(1, prefix_length+1):
        case_data = []
        case_data.append(case)
        case_data.append(event_length)
        remaining_time = calculate_remaining_time(df, event_length)
        case_data.append(remaining_time)
        elapsed_time = calculate_elapsed_time(df, event_length)
        case_data.append(elapsed_time)

        case_events = df[df['event_nr'] <= event_length]['activity_name'].tolist()
        __add_case_data(df, case_events, case_data, additional_columns, encoding)

        encoded_data.append(case_data)

    df = pd.DataFrame(columns=columns, data=encoded_data)
    return df


def __create_columns(prefix_length, additional_columns, encoding):
    if encoding == 'complex':
        return __create_complex_columns(prefix_length, additional_columns)
    elif encoding == 'frequency':
        return __create_index_latest_columns(prefix_length, additional_columns)


def __create_complex_columns(prefix_length, additional_columns):
    columns = list(DEFAULT_COLUMNS)
    for i in range(1, prefix_length + 1):
        columns.append("prefix_" + str(i))
        for additional_column in additional_columns:
            columns.append(additional_column + "_" + str(i))
    return columns


def __create_index_latest_columns(prefix_length, additional_columns):
    max_length = prefix_length + 1
    columns = list(DEFAULT_COLUMNS)
    for i in range(1, max_length):
        columns.append("prefix_" + str(i))
    for additional_column in additional_columns:
        columns.append(additional_column)
    return columns


def __add_case_data(df, case_events, case_data, additional_columns, encoding):
    if encoding == 'complex':
        return __complex_case_data(df, case_events, case_data, additional_columns)
    elif encoding == 'frequency':
        return __index_latest_case_data(df, case_events, case_data, additional_columns)


def __complex_case_data(df, case_events, case_data, additional_columns):
    for index in range(0, len(case_events)):
        case_data.append(case_events[index])
        __add_additional_columns(df, case_events, case_data, additional_columns)


def __index_latest_case_data(df, case_events, case_data, additional_columns):
    for index in range(0, len(case_events)):
        case_data.append(case_events[index])
    __add_additional_columns(df, case_events, case_data, additional_columns)


def __add_additional_columns(df, case_events, case_data, additional_columns):
    for additional_column in additional_columns:
        event_attribute = df[df['event_nr'] == len(case_events)][additional_column].apply(str).item()
        case_data.append(event_attribute)
