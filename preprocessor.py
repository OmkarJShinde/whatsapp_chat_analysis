import re
import pandas as pd

def preprocess(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][Mm])\s-\s'

    # Extract only date-time strings from messages
    dates = re.findall(pattern, data)

    # Extract user messages (remove date-time part)
    messages = re.sub(pattern, '', data).split("\n")  # Splitting messages

    # Ensure extracted lists are of the same length 
    while len(messages) > len(dates):
        dates.append(None)  # Fill missing dates with None for alignment

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Drop rows where 'message_date' is None (Non-timestamped messages)
    df.dropna(subset=['message_date'], inplace=True)

    # Normalize spaces before parsing
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=True)

        # Convert to datetime with proper format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p', errors='coerce')

    # Rename column 
    df.rename(columns={'message_date': 'date'}, inplace=True)


    # Separate Users and Messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([^:]+):\s', message)  # Correct regex
        if entry[1:]:
            users.append(entry[1])   # Extract Username
            messages.append(entry[2])  # Extract Message
        else:
            users.append('group_notification')
            messages.append(entry[0])


    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # period = []
    # for hour in df[['day_name', 'hour']]['hour']:
    #     if hour == 23:
    #         period.append(str(hour) + "-" + str('00'))
    #     elif hour == 0:
    #         period.append(str('00') + "-" + str(hour + 1))
    #     else:
    #         period.append(str(hour) + "-" + str(hour + 1))

    # df['period'] = period

    return df