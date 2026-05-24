import requests
import datetime
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import uuid
import json


file_lock = Lock()

def write_data(data):
    with file_lock:
        with open('email_match_linkedin.json', 'a') as f:
            f.write(json.dumps(data) + '\n')


def get_author_main(smtp, token):
    session = requests.Session()
    paramsGet = {
        "AadObjectId": "",
        "Smtp": smtp,
        "OlsPersonaId": "",
        "UserPrincipalName": "",
        "RootCorrelationId": str(uuid.uuid4()),
        "CorrelationId": str(uuid.uuid4()),
        "ClientCorrelationId": str(uuid.uuid4()),
        "PersonaDisplayName": "",
        "UserLocale": "en-US",
        "ExternalPageInstance": "00000000-0000-0000-0000-000000000000",
        "PersonaType": "User"
    }
    headers = {
        "Authorization": token,
        "X-ClientFeature": "LivePersonaCard",
        "Accept": "text/plain, application/json, text/json",
        "X-ClientType": "OwaMail",
        "X-HostAppCapabilities": "{}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Connection": "close",
        "X-LPCVersion": "1.20210418.1.0"
    }

    response = session.get(
        "https://sfnam.loki.delve.office.com/api/v1/linkedin/profiles/full",
        params=paramsGet,
        headers=headers
    )

    write_data({'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'token': token, 'email': smtp,
                "status": response.status_code,
                "response": response.text,})
    return 0

df_tokens = pd.read_json('access_token.json', lines=True)
df_tokens = df_tokens[(df_tokens['time'].str.contains(datetime.datetime.now().strftime("%Y-%m-%d")))].sort_values('time').drop_duplicates('account',keep='last')
df_tokens = df_tokens[df_tokens['status_code']==200]
# df_tokens.head()

df_emails = pd.read_excel('resource/email.xlsx')
# df_emails.head()

import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import itertools

# Assuming df_tokens and df_emails are already defined
tokens = df_tokens['authorization'].tolist()
emails = df_emails['email'].tolist()

# Function to get token in a round-robin fashion
def get_token(token_list):
    token_cycle = itertools.cycle(token_list)  # Cycle through tokens endlessly
    while True:
        yield next(token_cycle)


# Track total progress
total_tasks = len(emails)

# Create a tqdm progress bar
progress_bar = tqdm(total=total_tasks, desc="Processing emails", unit="email")

# Initialize token generator
token_generator = get_token(tokens)

for i_e in range(0, len(emails), 800):
    with ThreadPoolExecutor(max_workers=800) as executor:
        futures = [
            executor.submit(get_author_main, emails[i], next(token_generator)) 
            for i in range(i_e, min(i_e + 800, len(emails)))
        ]
        for future in as_completed(futures):
            future.result()
            progress_bar.update(1)

progress_bar.close()
print("All tasks completed.")