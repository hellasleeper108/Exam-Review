"""Flashcard mode - review concepts at your own pace."""

import random
from .base import GameMode
from utils.display import clear_screen, print_header, print_question
from utils.course_loader import Course


class FlashcardsMode(GameMode):
    """Flashcard mode for self-paced review."""

    def play(self, course: Course):
        """Run flashcard review session."""
        clear_screen()
        print_header(f"FLASHCARDS - {course.name}")

        questions = course.questions
        if not questions:
            print("No questions available for this course!")
            input("\nPress Enter to continue...")
            return

        # Shuffle questions
        random.shuffle(questions)

        print(f"Total cards: {len(questions)}")
        print("\nCommands: [s]how answer, [n]ext card, [q]uit\n")

        cards_reviewed = 0

        for i, question in enumerate(questions, 1):
            clear_screen()
            print_header(f"Card {i}/{len(questions)}")

            # Show lesson and difficulty
            if question.get('lesson'):
                print(f"Lesson: {question.get('lesson')}")
            if question.get('difficulty'):
                print(f"Difficulty: {question.get('difficulty').upper()}")
            print()

            # Show question
            print(f"Q: {question.get('question', '')}\n")

            # Wait for user command
            while True:
                command = self.get_user_input(
                    "What would you like to do? ",
                    valid_options=['s', 'show', 'n', 'next', 'q', 'quit']
                )

                if command in ['q', 'quit']:
                    print(f"\nYou reviewed {cards_reviewed} cards. Great work!")
                    input("\nPress Enter to continue...")
                    return

                if command in ['s', 'show']:
                    # Show answer
                    print(f"\nA: {question.get('answer', '')}")

                    if question.get('explanation'):
                        print(f"\nExplanation: {question.get('explanation')}")

                    print()

                if command in ['n', 'next']:
                    cards_reviewed += 1
                    break

        print(f"\n{'=' * 50}")
        print(f"Session complete! You reviewed {cards_reviewed} cards.")
        print(f"{'=' * 50}")
        input("\nPress Enter to continue...")
