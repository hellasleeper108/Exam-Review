"""Sudden death mode - one mistake and you're out!"""

import random
import time
from .base import GameMode
from utils.display import clear_screen, print_header
from utils.course_loader import Course
from utils.progress_tracker import ProgressTracker
from utils.encouragements import get_correct_answer_message, get_level_up_message


class SuddenDeathMode(GameMode):
    """Sudden death mode - one wrong answer ends the game."""

    def play(self, course: Course):
        """Run sudden death challenge."""
        tracker = ProgressTracker()
        start_time = time.time()

        clear_screen()
        print_header(f"SUDDEN DEATH - {course.name}")

        # Filter for multiple choice questions
        questions = [q for q in course.questions if q.get('type') == 'multiple_choice']

        if not questions:
            print("No multiple choice questions available for this course!")
            input("\nPress Enter to continue...")
            return

        # Shuffle questions
        random.shuffle(questions)

        print("⚠️  WARNING: One wrong answer and it's GAME OVER! ⚠️")
        print(f"\nTotal questions available: {len(questions)}")
        print("How many can you get right in a row?\n")
        input("Press Enter to start... if you dare!")

        streak = 0
        total_xp_earned = 0

        for i, question in enumerate(questions, 1):
            clear_screen()
            print_header(f"SUDDEN DEATH - Streak: {streak}")

            # Show difficulty
            if question.get('difficulty'):
                diff = question.get('difficulty').upper()
                print(f"Difficulty: {diff}")
            print()

            # Show question and choices
            print(f"{question.get('question', '')}\n")
            choices = question.get('choices', [])

            for j, choice in enumerate(choices, 1):
                print(f"{j}. {choice}")

            # Get user answer
            while True:
                try:
                    answer_num = input("\nYour answer (or 'q' to quit while ahead): ").strip()

                    if answer_num.lower() == 'q':
                        duration = int(time.time() - start_time)
                        tracker.record_session(course.name, 'Sudden Death', streak, streak, duration)

                        clear_screen()
                        print_header("FINAL SCORE")
                        self.show_final_results(streak, total_xp_earned, stopped_early=True)
                        input("\nPress Enter to continue...")
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
            correct_answer = question.get('answer', '')
            difficulty = question.get('difficulty', 'easy')
            is_correct = user_answer == correct_answer

            xp_earned, leveled_up = tracker.record_answer(
                course.name,
                question.get('lesson', 'Unknown'),
                question.get('question', ''),
                is_correct,
                difficulty,
                'Sudden Death'
            )

            if is_correct:
                streak += 1
                total_xp_earned += xp_earned
                print(f"\n✓ {get_correct_answer_message()} +{xp_earned} XP")
                print("You survive... for now.")
                if leveled_up:
                    input("\nPress Enter to see your reward...")
                    clear_screen()
                    print_level_up_banner(tracker.data['level'])
                input("\nPress Enter to continue...")
            else:
                # GAME OVER - Record session and show results
                duration = int(time.time() - start_time)
                tracker.record_session(course.name, 'Sudden Death', streak, streak + 1, duration)

                clear_screen()
                print_header("💀 GAME OVER 💀")
                print(f"\n✗ Wrong! The correct answer was: {correct_answer}\n")

                if question.get('explanation'):
                    print(f"Explanation: {question.get('explanation')}\n")

                self.show_final_results(streak, total_xp_earned, stopped_early=False)
                input("\nPress Enter to continue...")
                return

        # If they somehow answer all questions correctly
        duration = int(time.time() - start_time)
        tracker.record_session(course.name, 'Sudden Death', streak, streak, duration)

        clear_screen()
        print_header("🏆 PERFECT SCORE! 🏆")
        print(f"\nIncredible! You answered all {streak} questions correctly!")
        print(f"💰 Total XP Earned: {total_xp_earned}")
        print("You are a TRUE MASTER!")
        input("\nPress Enter to continue...")

    def show_final_results(self, streak: int, total_xp: int, stopped_early: bool):
        """Display final results with commentary."""
        print(f"Final Streak: {streak} correct answer{'s' if streak != 1 else ''}")
        print(f"💰 Total XP Earned: {total_xp}")
        print("=" * 40)

        if stopped_early:
            print("\nYou quit while you were ahead. Smart move!")

        if streak == 0:
            print("\nOof. Better luck next time!")
        elif streak == 1:
            print("\nWell, at least you got one right!")
        elif streak < 5:
            print("\nNot bad for sudden death mode!")
        elif streak < 10:
            print("\nImpressive! You're really getting the hang of this.")
        elif streak < 20:
            print("\nOutstanding performance! You're a sudden death survivor!")
        else:
            print("\nLEGENDARY! You're unstoppable!")
