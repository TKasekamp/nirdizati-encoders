import pandas as pd

from nirdizati.encoders.helper import *


def encode_trace(data, prefix_length=1):
    events = get_events(data).tolist()
    cases = get_cases(data)

    columns = __create_columns(prefix_length)
    encoded_data = []

    for case in cases:
        df = data[data['case_id'] == case]
        event_length = prefix_length
        case_data = []
        case_data.append(case)
        case_data.append(event_length)
        remaining_time = calculate_remaining_time(df, event_length)
        case_data.append(remaining_time)
        elapsed_time = calculate_elapsed_time(df, event_length)
        case_data.append(elapsed_time)

        case_events = df[df['event_nr'] <= event_length]['activity_name'].tolist()
        for e in case_events:
            case_data.append(events.index(e) + 1)
        encoded_data.append(case_data)

    df = pd.DataFrame(columns=columns, data=encoded_data)
    return df


def __create_columns(prefix_length):
    columns = list(DEFAULT_COLUMNS)
    for i in range(1, prefix_length + 1):
        columns.append("prefix_" + str(i))
    return columns
