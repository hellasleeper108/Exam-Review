#!/usr/bin/env python3
"""
Exam Review Game - Main Entry Point
Choose your course and game mode to start studying!
"""

import os
import sys
import json
from pathlib import Path

# Add project modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_modes.flashcards import FlashcardsMode
from game_modes.quiz import QuizMode
from game_modes.timed import TimedChallengeMode
from game_modes.sudden_death import SuddenDeathMode
from utils.course_loader import CourseLoader
from utils.display import clear_screen, print_header, print_menu


def main():
    """Main entry point for the exam review application."""
    clear_screen()
    print_header("EXAM REVIEW GAME")

    # Initialize course loader
    courses_dir = Path(__file__).parent / "courses"
    loader = CourseLoader(courses_dir)

    # Main loop
    while True:
        # Course selection
        course = select_course(loader)
        if course is None:
            print("\nThanks for studying! Good luck on your exam!")
            break

        # Game mode selection
        game_mode = select_game_mode()
        if game_mode is None:
            continue

        # Start the selected game mode
        game_mode.play(course)

        # Ask if user wants to continue
        print("\n")
        choice = input("Return to main menu? (y/n): ").strip().lower()
        if choice != 'y':
            print("\nThanks for studying! Good luck on your exam!")
            break


def select_course(loader):
    """Display course menu and return selected course."""
    clear_screen()
    print_header("SELECT COURSE")

    courses = loader.get_available_courses()

    if not courses:
        print("No courses found! Please add course files to the 'courses' directory.")
        input("\nPress Enter to exit...")
        return None

    print_menu(courses)
    print(f"{len(courses) + 1}. Exit")

    while True:
        try:
            choice = input("\nSelect course number: ").strip()
            choice_num = int(choice)

            if choice_num == len(courses) + 1:
                return None

            if 1 <= choice_num <= len(courses):
                course_file = courses[choice_num - 1]
                return loader.load_course(course_file)
            else:
                print(f"Please enter a number between 1 and {len(courses) + 1}")
        except ValueError:
            print("Please enter a valid number")
        except Exception as e:
            print(f"Error loading course: {e}")
            input("\nPress Enter to continue...")
            return None


def select_game_mode():
    """Display game mode menu and return selected game mode instance."""
    clear_screen()
    print_header("SELECT GAME MODE")

    modes = [
        ("Flashcards", "Review concepts at your own pace", FlashcardsMode),
        ("Multiple Choice Quiz", "Test your knowledge with quizzes", QuizMode),
        ("Timed Challenge", "Race against the clock!", TimedChallengeMode),
        ("Sudden Death", "One mistake and you're out!", SuddenDeathMode),
    ]

    for i, (name, description, _) in enumerate(modes, 1):
        print(f"{i}. {name}")
        print(f"   {description}\n")

    print(f"{len(modes) + 1}. Back to course selection")

    while True:
        try:
            choice = input("\nSelect game mode: ").strip()
            choice_num = int(choice)

            if choice_num == len(modes) + 1:
                return None

            if 1 <= choice_num <= len(modes):
                _, _, mode_class = modes[choice_num - 1]
                return mode_class()
            else:
                print(f"Please enter a number between 1 and {len(modes) + 1}")
        except ValueError:
            print("Please enter a valid number")


if __name__ == "__main__":
    main()
