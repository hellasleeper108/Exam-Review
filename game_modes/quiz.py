"""Multiple choice quiz mode."""

import random
import time
from .base import GameMode
from utils.display import clear_screen, print_header, print_score
from utils.course_loader import Course
from utils.progress_tracker import ProgressTracker
from utils.splash import print_level_up_banner
from utils.encouragements import (
    get_correct_answer_message,
    get_wrong_answer_message,
    get_level_up_message,
    get_streak_message
)


class QuizMode(GameMode):
    """Multiple choice quiz mode."""

    def play(self, course: Course):
        """Run multiple choice quiz."""
        tracker = ProgressTracker()
        start_time = time.time()

        clear_screen()
        print_header(f"QUIZ MODE - {course.name}")

        # Show current level and XP
        stats = tracker.get_stats()
        print(f"Level {stats['level']} | {stats['total_xp']} XP")
        tracker.display_progress_bar()

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
        streak = 0
        total_xp_earned = 0

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
            is_correct = user_answer == correct_answer
            difficulty = question.get('difficulty', 'easy')

            # Record answer and award XP
            xp_earned, leveled_up = tracker.record_answer(
                course.name,
                question.get('lesson', 'Unknown'),
                question.get('question', ''),
                is_correct,
                difficulty,
                'Quiz'
            )

            if is_correct:
                correct += 1
                streak += 1
                total_xp_earned += xp_earned

                # Show encouraging message
                print(f"\n✓ {get_correct_answer_message()}")
                print(f"   +{xp_earned} XP")

                # Check for streak milestone
                streak_msg = get_streak_message(streak)
                if streak_msg:
                    print(f"   {streak_msg}")

                # Check for level up
                if leveled_up:
                    input("\nPress Enter to see your reward...")
                    clear_screen()
                    print_level_up_banner(tracker.data['level'])
                    input("Press Enter to continue...")
            else:
                streak = 0  # Reset streak
                print(f"\n✗ {get_wrong_answer_message()}")
                print(f"   The correct answer is: {correct_answer}")

            if question.get('explanation'):
                print(f"\n💡 Explanation: {question.get('explanation')}")

            input("\nPress Enter for next question...")

        # Calculate duration
        duration = int(time.time() - start_time)

        # Record session
        tracker.record_session(course.name, 'Quiz', correct, total, duration)

        # Show final score
        clear_screen()
        print_header("QUIZ COMPLETE")
        print_score(correct, total)

        # Show XP earned
        print(f"💰 Total XP Earned: {total_xp_earned}")
        print(f"⏱️  Time: {duration // 60}m {duration % 60}s")
        print()

        # Show updated level
        stats = tracker.get_stats()
        print(f"Current Level: {stats['level']} ({stats['total_xp']} total XP)")
        tracker.display_progress_bar()

        # Performance feedback
        percentage = (correct / total * 100) if total > 0 else 0
        if percentage >= 90:
            print("🌟 Outstanding! You're really mastering this material!")
        elif percentage >= 70:
            print("👍 Good job! Keep practicing to improve even more.")
        elif percentage >= 50:
            print("📚 Not bad, but there's room for improvement. Review and try again!")
        else:
            print("💪 Keep studying! Review the material and come back stronger.")

        input("\nPress Enter to continue...")
