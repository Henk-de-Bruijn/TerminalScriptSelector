"""
JSON Pretty Formatter
Reads a JSON file, formats it nicely, and copies to clipboard.
"""

TITLE = "JSON Pretty Formatter"

DESCRIPTION = """Read JSON from a file or clipboard, format it beautifully, and copy to clipboard.

Usage:
  <json_file>    - Read from file
  clipboard      - Read from clipboard
  clip           - Read from clipboard (short)

Examples:
  data.json
  clipboard
  clip
  
Required packages: pyperclip
Install with: pip install pyperclip
"""

def run(args):
    """Format JSON and copy to clipboard."""
    import json
    import pyperclip

    if len(args) != 1:
        print("❌ Error: Expected 1 argument")
        print("Usage: <json_file> or 'clipboard'")
        print("Example: data.json")
        print("Example: clipboard")
        return

    input_source = args[0]

    try:
        # Determine input source
        if input_source.lower() in ['clipboard', 'clip', 'cb']:
            print("📋 Reading from clipboard...")
            json_string = pyperclip.paste()
            if not json_string.strip():
                print("❌ Error: Clipboard is empty")
                return
            data = json.loads(json_string)
            source_name = "clipboard"
        else:
            # Read JSON file
            print(f"📖 Reading {input_source}...")
            with open(input_source, 'r', encoding='utf-8') as f:
                data = json.load(f)
            source_name = input_source

        # Format with indentation
        formatted = json.dumps(data, indent=2, ensure_ascii=False)

        # Display formatted JSON
        print("\n" + "="*60)
        print("FORMATTED JSON:")
        print("="*60)
        print(formatted)
        print("="*60)

        # Ask if user wants to copy
        response = input("\n📋 Copy to clipboard? (y/n): ").strip().lower()

        if response in ['y', 'yes']:
            pyperclip.copy(formatted)
            print("✅ Copied to clipboard!")
        else:
            print("👍 Not copied.")

    except FileNotFoundError:
        print(f"❌ Error: File '{input_source}' not found")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
    except Exception as e:
        print(f"❌ Error: {e}")