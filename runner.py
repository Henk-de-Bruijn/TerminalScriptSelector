#!/usr/bin/env python3
"""
Terminal Snippet Runner
A simple tool to manage and execute Python snippets interactively.
"""

import os
import sys
import importlib.util
from pathlib import Path


class SnippetRunner:
    def __init__(self, snippets_dir="snippets"):
        self.snippets_dir = Path(snippets_dir)
        self.snippets = []

    def load_snippets(self):
        """Load all Python files from the snippets directory."""
        if not self.snippets_dir.exists():
            print(f"Creating snippets directory: {self.snippets_dir}")
            self.snippets_dir.mkdir(parents=True)
            return

        self.snippets = []
        for py_file in self.snippets_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue

            try:
                spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Each snippet must have TITLE, DESCRIPTION, and run() function
                if hasattr(module, 'TITLE') and hasattr(module, 'DESCRIPTION') and hasattr(module, 'run'):
                    self.snippets.append({
                        'name': py_file.stem,
                        'title': module.TITLE,
                        'description': module.DESCRIPTION,
                        'module': module
                    })
            except Exception as e:
                print(f"Error loading {py_file.name}: {e}")

        self.snippets.sort(key=lambda x: x['title'])

    def show_menu(self):
        """Display the main menu with available snippets."""
        print("\n" + "=" * 60)
        print("  SNIPPET RUNNER")
        print("=" * 60)

        if not self.snippets:
            print("\nNo snippets found in the 'snippets' directory.")
            print("Add .py files to get started!")
            return False

        print("\nAvailable Tools:")
        for i, snippet in enumerate(self.snippets, 1):
            print(f"  {i}. {snippet['title']}")

        print(f"\n  0. Exit")
        print("=" * 60)
        return True

    def get_choice(self):
        """Get user's menu choice."""
        while True:
            try:
                choice = input("\nSelect a tool (number): ").strip()
                choice_num = int(choice)

                if choice_num == 0:
                    return None

                if 1 <= choice_num <= len(self.snippets):
                    return choice_num - 1

                print(f"Please enter a number between 0 and {len(self.snippets)}")
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                print("\n")
                return None

    def run_snippet(self, snippet_idx):
        """Run the selected snippet."""
        snippet = self.snippets[snippet_idx]

        print("\n" + "-" * 60)
        print(f"  {snippet['title']}")
        print("-" * 60)
        print(f"\n{snippet['description']}\n")

        while True:
            try:
                command = input("Enter command (or 'back' to return): ").strip()

                if command.lower() in ['back', 'b', 'exit']:
                    break

                if not command:
                    continue

                # Parse command into arguments
                args = command.split()

                # Run the snippet
                try:
                    snippet['module'].run(args)
                except Exception as e:
                    print(f"\n❌ Error: {e}")

                # Ask what to do next
                print("\n" + "-" * 60)
                next_action = input("\nWhat next? (r)un again, (b)ack to menu, (q)uit: ").strip().lower()

                if next_action in ['b', 'back', 'm', 'menu']:
                    break
                elif next_action in ['q', 'quit', 'exit']:
                    return False
                # Otherwise loop and run again

            except KeyboardInterrupt:
                print("\n")
                break

        return True

    def run(self):
        """Main application loop."""
        print("\nWelcome to Snippet Runner!")

        while True:
            self.load_snippets()

            if not self.show_menu():
                print("\nAdd snippet files to the 'snippets' directory and restart.")
                break

            choice = self.get_choice()

            if choice is None:
                print("\nGoodbye!")
                break

            if not self.run_snippet(choice):
                print("\nGoodbye!")
                break


def main():
    runner = SnippetRunner()
    runner.run()


if __name__ == "__main__":
    main()