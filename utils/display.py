"""Display utilities for terminal UI."""

import os


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(text: str):
    """Print a formatted header."""
    width = max(60, len(text) + 4)
    print("=" * width)
    print(text.center(width))
    print("=" * width)
    print()


def print_menu(items: list):
    """Print a numbered menu."""
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")
    print()


def print_question(question_data: dict, show_answer: bool = False):
    """Print a formatted question."""
    print(f"\nQuestion: {question_data.get('question', '')}")

    if question_data.get('type') == 'multiple_choice':
        choices = question_data.get('choices', [])
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")

    if show_answer:
        print(f"\nAnswer: {question_data.get('answer', '')}")

        if question_data.get('explanation'):
            print(f"Explanation: {question_data.get('explanation')}")


def print_score(correct: int, total: int):
    """Print formatted score."""
    percentage = (correct / total * 100) if total > 0 else 0
    print(f"\n{'=' * 40}")
    print(f"Score: {correct}/{total} ({percentage:.1f}%)")
    print(f"{'=' * 40}\n")
