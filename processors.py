# processors.py - purely processing functions

import pandas as pd
import io

def process_csv_content(file_bytes: bytes, max_rows: int = 50) -> dict:
    """Process CSV bytes and return structured data - optimized"""
    df = pd.read_csv(io.BytesIO(file_bytes))
    
    # Truncate if too many rows
    if len(df) > max_rows:
        df_sample = df.head(max_rows)
        row_info = f"{max_rows} of {len(df)} rows (truncated)"
    else:
        df_sample = df
        row_info = f"{len(df)} rows"
    
    # Create compact summary
    summary = f"""
    CSV Data Analysis Request:
    - File Shape: {len(df)} rows × {len(df.columns)} columns
    - Column Names: {', '.join(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}
    - Data Sample (first {min(3, len(df_sample))} rows):
    {df_sample.head(3).to_string(index=False, max_colwidth=30)}
    """
    
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "summary": summary.strip()
    }