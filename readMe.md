# Snippet Runner

A simple, interactive terminal application for managing and running your Python code snippets. Keep your useful scripts organized and run them with ease!

## Features

- 📁 **Modular snippet system** - Each tool is a separate Python file
- 🎯 **Interactive menu** - Easy-to-use selection interface
- 📋 **Built-in guides** - Each snippet shows usage instructions
- 🔄 **Smart navigation** - Run multiple times or return to menu
- ⚡ **Easy to extend** - Add new snippets in seconds

## Installation

1. **Clone or download** the files to your local machine

2. **Install dependencies:**
   ```bash
   pip install pandas openpyxl pyperclip
   ```

3. **Run the application:**
   ```bash
   python runner.py
   ```

## Usage

1. Start the runner: `python runner.py`
2. Select a tool by entering its number
3. Read the usage guide displayed
4. Enter your command with arguments
5. After execution, choose to:
   - `r` - Run again
   - `b` - Back to menu
   - `q` - Quit

## Included Snippets

### CSV to Excel Converter
Convert CSV files with custom delimiters or transform between different formats.

**Examples:**
```bash
data.csv output.xlsx comma              # Comma CSV to Excel
data.csv output.csv comma tab           # Convert comma to tab-delimited
clipboard output.xlsx semicolon         # Clipboard to Excel
data.csv clipboard tab comma            # File to clipboard as comma-delimited
```

### JSON Pretty Formatter
Read JSON from files or clipboard, format it beautifully, and optionally copy to clipboard.

**Examples:**
```bash
data.json                # Format JSON file
clipboard                # Format JSON from clipboard
config.json              # Format and optionally copy
```

## Creating Your Own Snippets

Adding a new snippet is simple! Create a new `.py` file in the `snippets/` folder with this structure:

```python
"""
Your snippet description
"""

TITLE = "My Awesome Tool"

DESCRIPTION = """
Brief description of what your tool does.

Usage:
  <arg1> <arg2> [optional_arg]

Examples:
  example1.txt output.txt
  data.json
"""

def run(args):
    """
    Main function that runs your snippet.
    
    Args:
        args: List of command-line arguments (strings)
    """
    # Validate arguments
    if len(args) != 2:
        print("❌ Error: Expected 2 arguments")
        print("Usage: <input> <output>")
        return
    
    input_file, output_file = args
    
    try:
        # Your code here
        print(f"✅ Success!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
```

### Snippet Guidelines

- **TITLE**: Short, descriptive name shown in the menu
- **DESCRIPTION**: Multi-line string with usage instructions and examples
- **run(args)**: Function that receives a list of string arguments
- Use emoji for visual feedback (✅ ❌ 📖 💾 📋)
- Handle errors gracefully and provide helpful messages
- Import dependencies inside the `run()` function

## Project Structure

```
.
├── runner.py                  # Main application
├── snippets/                  # Snippet directory
│   ├── csv_to_excel.py       # CSV converter
│   ├── json_formatter.py     # JSON formatter
│   └── your_snippet.py       # Your custom snippets
└── README.md                  # This file
```

## Tips

- **Quick access**: Create an alias in your shell:
  ```bash
  alias snippets='python /path/to/runner.py'
  ```

- **Clipboard shortcuts**: Use `clip` or `cb` instead of typing `clipboard`

- **Add to PATH**: Make the runner available system-wide (optional)

- **Share snippets**: The modular design makes it easy to share individual snippets with others

## Troubleshooting

**"No snippets found"**
- Make sure `.py` files are in the `snippets/` folder
- Check that files have `TITLE`, `DESCRIPTION`, and `run()` function

**Import errors**
- Install required packages: `pip install pandas openpyxl pyperclip`
- Add package installation notes to your snippet's `DESCRIPTION`

**Snippet not appearing in menu**
- File names starting with `_` are ignored
- Restart the runner to reload snippets
- Check for syntax errors in your snippet file

## Contributing

Have a useful snippet? Feel free to add it to your local collection! Common ideas:

- File converters (PDF, images, formats)
- Text processors (regex tools, formatters)
- API helpers (quick API calls, auth testers)
- Data validators (schema checkers, sanitizers)
- Quick calculators (conversions, formulas)

## License

Free to use and modify for your personal projects!

---

**Happy snippet running! 🚀**