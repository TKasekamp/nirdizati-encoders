import numpy as np
import pandas as pd

import encoder


def encode_trace(data):
    data_encoder = encoder.Encoder()
    events = data_encoder.get_events(data)
    cases = data_encoder.get_cases(data)

    columns = events
    columns = np.append(events, ["case_id", "event_nr", "remaining_time", "elapsed_time"])
    encoded_data = pd.DataFrame(columns=columns)

    i = 0
    for case in cases:
        df = data[data['case_id'] == case]
        for j in range(0, max(df['event_nr'])):
            case_data = []
            event_length = j + 1
            for event in events:
                case_data.append(len(df[(df['activity_name'] == event) & (df['event_nr'] <= event_length)]))
            case_data.append(case)
            case_data.append(event_length)
            remaining_time = data_encoder.calculate_remaining_time(df, event_length)
            case_data.append(remaining_time)
            elapsed_time = data_encoder.calculate_elapsed_time(df, event_length)
            case_data.append(elapsed_time)
            encoded_data.loc[i] = case_data
            i = i + 1

    return encoded_data
