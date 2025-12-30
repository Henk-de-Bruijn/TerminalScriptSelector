"""
ToDo Manager
Manage your todo list with priorities and status tracking.
"""

TITLE = "ToDo Manager"

DESCRIPTION = """Manage your todo list with priorities and status tracking.

Commands:
  list                           - Show all todos
  add <title> [priority]        - Add new todo (priority is optional number)
  status <priority> <status>    - Change status (todo/progress/done)
  remove <priority>             - Remove a todo

Status values:
  - todo (default)
  - progress (or in-progress, inprogress)
  - done (or completed, complete)

Examples:
  list
  add "Fix bug in login" 1
  add "Update documentation"
  status 3 progress
  status 5 done
  remove 2

Note: Priority is used as the identifier for updating/removing todos.
Storage: Data saved in snippets/data/todos.json
"""


def run(args):
    """Manage todos."""
    import json
    from pathlib import Path
    from datetime import datetime

    # Setup data directory and file
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    todo_file = data_dir / "todos.json"

    # Status mapping
    status_map = {
        'todo': 'todo',
        'progress': 'in progress',
        'in-progress': 'in progress',
        'inprogress': 'in progress',
        'done': 'completed',
        'completed': 'completed',
        'complete': 'completed',
    }

    def load_todos():
        """Load todos from file."""
        if not todo_file.exists():
            return []
        try:
            with open(todo_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def save_todos(todos):
        """Save todos to file."""
        with open(todo_file, 'w', encoding='utf-8') as f:
            json.dump(todos, f, indent=2, ensure_ascii=False)

    def show_todos(todos):
        """Display all todos in a formatted table."""
        if not todos:
            print("\n📋 No todos yet! Add one with: add <title> [priority]")
            return

        print("\n" + "=" * 90)
        print(f"{'PRI':<5} {'TITLE':<45} {'DATE':<17} {'STATUS':<12}")
        print("=" * 90)

        for todo in todos:
            status_emoji = {
                'todo': '⭕',
                'in progress': '🔄',
                'completed': '✅'
            }.get(todo['status'], '⭕')

            print(f"{todo['priority']:<5} {todo['title']:<45} "
                  f"{todo['date']:<17} {status_emoji} {todo['status']:<10}")

        print("=" * 90)
        print(f"Total: {len(todos)} todos\n")

    def get_next_priority(todos):
        """Get next priority (lowest number not used)."""
        if not todos:
            return 1
        used_priorities = {todo['priority'] for todo in todos}
        priority = 1
        while priority in used_priorities:
            priority += 1
        return priority

    # Parse command
    if len(args) == 0:
        print("❌ Error: No command specified")
        print("Usage: list | add <title> [priority] | status <priority> <status> | remove <priority>")
        return

    command = args[0].lower()
    todos = load_todos()

    try:
        if command == 'list':
            show_todos(todos)

        elif command == 'add':
            if len(args) < 2:
                print("❌ Error: Missing title")
                print("Usage: add <title> [priority]")
                return

            # Parse title and priority
            if len(args) >= 3 and args[-1].isdigit():
                # Last argument is priority
                priority = int(args[-1])
                title = ' '.join(args[1:-1])

                # Shift existing todos with same or lower priority down
                for todo in todos:
                    if todo['priority'] >= priority:
                        todo['priority'] += 1
            else:
                # No priority specified, use next available
                priority = get_next_priority(todos)
                title = ' '.join(args[1:])

            # Remove quotes if present
            title = title.strip('"').strip("'")

            new_todo = {
                'title': title,
                'status': 'todo',
                'priority': priority,
                'date': datetime.now().strftime('%d %b %H:%M')
            }

            todos.append(new_todo)
            # Sort by priority
            todos.sort(key=lambda x: x['priority'])
            save_todos(todos)

            print(f"✅ Added todo [Priority {priority}]: {title}")
            if any(todo['priority'] > priority for todo in todos):
                print(f"   (Shifted lower priority items down)")

        elif command == 'status':
            if len(args) != 3:
                print("❌ Error: Expected <priority> <status>")
                print("Usage: status <priority> <status>")
                print("Status: todo | progress | done")
                return

            try:
                priority = int(args[1])
            except ValueError:
                print(f"❌ Error: Invalid priority '{args[1]}'")
                return

            new_status = status_map.get(args[2].lower())
            if not new_status:
                print(f"❌ Error: Invalid status '{args[2]}'")
                print("Valid statuses: todo | progress | done")
                return

            # Find and update todo
            found = False
            for todo in todos:
                if todo['priority'] == priority:
                    old_status = todo['status']
                    todo['status'] = new_status
                    found = True
                    break

            if not found:
                print(f"❌ Error: Todo with priority {priority} not found")
                return

            save_todos(todos)
            print(f"✅ Updated todo [Priority {priority}]: {old_status} → {new_status}")

        elif command == 'remove':
            if len(args) != 2:
                print("❌ Error: Expected <priority>")
                print("Usage: remove <priority>")
                return

            try:
                priority = int(args[1])
            except ValueError:
                print(f"❌ Error: Invalid priority '{args[1]}'")
                return

            # Find and remove todo
            original_count = len(todos)
            todos = [todo for todo in todos if todo['priority'] != priority]

            if len(todos) == original_count:
                print(f"❌ Error: Todo with priority {priority} not found")
                return

            save_todos(todos)
            print(f"✅ Removed todo [Priority {priority}]")

        else:
            print(f"❌ Error: Unknown command '{command}'")
            print("Available commands: list | add | status | remove")

    except Exception as e:
        print(f"❌ Error: {e}")