"""Multiple choice quiz mode."""

import random
from .base import GameMode
from utils.display import clear_screen, print_header, print_score
from utils.course_loader import Course


class QuizMode(GameMode):
    """Multiple choice quiz mode."""

    def play(self, course: Course):
        """Run multiple choice quiz."""
        clear_screen()
        print_header(f"QUIZ MODE - {course.name}")

        # Filter for multiple choice questions
        questions = [q for q in course.questions if q.get('type') == 'multiple_choice']

        if not questions:
            print("No multiple choice questions available for this course!")
            input("\nPress Enter to continue...")
            return

        # Shuffle questions
        random.shuffle(questions)

        print(f"Total questions: {len(questions)}")
        print("Answer each question by entering the number of your choice.\n")
        input("Press Enter to start...")

        correct = 0
        total = 0

        for i, question in enumerate(questions, 1):
            clear_screen()
            print_header(f"Question {i}/{len(questions)}")

            # Show lesson and difficulty
            if question.get('lesson'):
                print(f"Lesson: {question.get('lesson')}")
            if question.get('difficulty'):
                print(f"Difficulty: {question.get('difficulty').upper()}")
            print()

            # Show question and choices
            print(f"{question.get('question', '')}\n")
            choices = question.get('choices', [])

            for j, choice in enumerate(choices, 1):
                print(f"{j}. {choice}")

            # Get user answer
            while True:
                try:
                    answer_num = input("\nYour answer (or 'q' to quit): ").strip()

                    if answer_num.lower() == 'q':
                        print_score(correct, total)
                        input("Press Enter to continue...")
                        return

                    answer_num = int(answer_num)

                    if 1 <= answer_num <= len(choices):
                        user_answer = choices[answer_num - 1]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(choices)}")
                except ValueError:
                    print("Please enter a valid number or 'q' to quit")

            # Check answer
            total += 1
            correct_answer = question.get('answer', '')

            if user_answer == correct_answer:
                correct += 1
                print("\n✓ Correct!")
            else:
                print(f"\n✗ Incorrect. The correct answer is: {correct_answer}")

            if question.get('explanation'):
                print(f"\nExplanation: {question.get('explanation')}")

            input("\nPress Enter for next question...")

        # Show final score
        clear_screen()
        print_header("QUIZ COMPLETE")
        print_score(correct, total)

        # Performance feedback
        percentage = (correct / total * 100) if total > 0 else 0
        if percentage >= 90:
            print("Outstanding! You're really mastering this material!")
        elif percentage >= 70:
            print("Good job! Keep practicing to improve even more.")
        elif percentage >= 50:
            print("Not bad, but there's room for improvement. Review and try again!")
        else:
            print("Keep studying! Review the material and come back stronger.")

        input("\nPress Enter to continue...")
