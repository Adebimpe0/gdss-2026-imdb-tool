# CSV/Excel Export Logic - GDSS 2026 Hackathon
# This module handles exporting extracted IMDB data to CSV or Excel

import pandas as pd
import io

def export_to_csv(data):
    df = pd.DataFrame([data])
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

def export_to_excel(data):
    df = pd.DataFrame([data])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='IMDB Data')
    output.seek(0)
    return output
