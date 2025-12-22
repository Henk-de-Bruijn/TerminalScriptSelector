"""
CSV to Excel Converter
Converts tab-delimited CSV files to Excel format.
"""

TITLE = "CSV to Excel Converter"

DESCRIPTION = """Convert a CSV file to Excel format with custom delimiter.

Usage:
  <input> <output> [delimiter]

Input/Output Options:
  - filename.csv    : Read from/write to file
  - clipboard/clip  : Read from/write to clipboard

Delimiter (optional):
  - tab (default)
  - comma or ,
  - semicolon or ;
  - pipe or |
  - Any single character

Examples:
  data.csv output.xlsx          # Tab-delimited file to Excel
  data.csv output.xlsx comma    # Comma-delimited file to Excel
  clipboard output.xlsx         # Clipboard to Excel file
  data.csv clipboard tab        # File to clipboard
  clipboard clipboard comma     # Clipboard to clipboard (reformats)

Required packages: pandas, openpyxl, pyperclip
Install with: pip install pandas openpyxl pyperclip
"""


def run(args):
    """Convert CSV to Excel."""
    import pandas as pd
    import pyperclip
    from io import StringIO, BytesIO

    if len(args) < 2 or len(args) > 3:
        print("❌ Error: Expected 2-3 arguments")
        print("Usage: <input> <output> [delimiter]")
        print("Example: data.csv output.xlsx")
        print("Example: clipboard output.xlsx comma")
        print("Example: data.csv clipboard tab")
        return

    input_source = args[0]
    output_dest = args[1]
    delimiter_arg = args[2] if len(args) == 3 else 'tab'

    # Map delimiter names to actual characters
    delimiter_map = {
        'tab': '\t',
        'comma': ',',
        ',': ',',
        'semicolon': ';',
        ';': ';',
        'pipe': '|',
        '|': '|',
        'space': ' ',
    }

    delimiter = delimiter_map.get(delimiter_arg.lower(), delimiter_arg)

    # Validate delimiter is a single character
    if len(delimiter) != 1:
        print(f"❌ Error: Delimiter must be a single character, got '{delimiter}'")
        return

    try:
        # Read input
        if input_source.lower() in ['clipboard', 'clip', 'cb']:
            print(f"📋 Reading from clipboard...")
            csv_data = pyperclip.paste()
            if not csv_data.strip():
                print("❌ Error: Clipboard is empty")
                return
            df = pd.read_csv(StringIO(csv_data), sep=delimiter)
            source_name = "clipboard"
        else:
            print(f"📖 Reading {input_source}...")
            df = pd.read_csv(input_source, sep=delimiter)
            source_name = input_source

        print(f"   Found {len(df)} rows and {len(df.columns)} columns")

        # Write output
        if output_dest.lower() in ['clipboard', 'clip', 'cb']:
            print(f"💾 Writing to clipboard...")
            # Convert to Excel in memory
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            # Note: We can't copy binary Excel to clipboard, so convert to CSV
            csv_output = df.to_csv(index=False, sep='\t')
            pyperclip.copy(csv_output)
            print(f"✅ Success! Copied as tab-delimited CSV to clipboard")
            print(f"   (Excel binary can't be copied to clipboard)")
        else:
            print(f"💾 Writing to {output_dest}...")
            df.to_excel(output_dest, index=False, engine='openpyxl')
            print(f"✅ Success! Created {output_dest}")

    except FileNotFoundError:
        print(f"❌ Error: File '{input_source}' not found")
    except pd.errors.ParserError as e:
        print(f"❌ Error: Failed to parse CSV - {e}")
        print(f"   Check if delimiter '{delimiter}' is correct")
    except Exception as e:
        print(f"❌ Error: {e}")