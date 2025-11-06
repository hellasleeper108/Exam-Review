"""Timed challenge mode - race against the clock!"""

import random
import time
from .base import GameMode
from utils.display import clear_screen, print_header, print_score
from utils.course_loader import Course
from utils.progress_tracker import ProgressTracker
from utils.encouragements import get_correct_answer_message, get_wrong_answer_message, get_level_up_message


class TimedChallengeMode(GameMode):
    """Timed challenge mode with time pressure."""

    def play(self, course: Course):
        """Run timed challenge."""
        tracker = ProgressTracker()
        session_start = time.time()

        clear_screen()
        print_header(f"TIMED CHALLENGE - {course.name}")

        # Filter for multiple choice questions
        questions = [q for q in course.questions if q.get('type') == 'multiple_choice']

        if not questions:
            print("No multiple choice questions available for this course!")
            input("\nPress Enter to continue...")
            return

        # Shuffle and limit questions
        random.shuffle(questions)
        num_questions = min(10, len(questions))  # Max 10 questions for timed mode
        questions = questions[:num_questions]

        time_limit = 30  # seconds per question

        print(f"Challenge: {num_questions} questions")
        print(f"Time limit: {time_limit} seconds per question")
        print("\nAnswer as many questions correctly as you can before time runs out!")
        input("\nPress Enter to start...")

        correct = 0
        total = 0
        total_xp_earned = 0

        for i, question in enumerate(questions, 1):
            clear_screen()
            print_header(f"Question {i}/{num_questions}")

            # Show difficulty
            if question.get('difficulty'):
                print(f"Difficulty: {question.get('difficulty').upper()}")
            print()

            # Show question and choices
            print(f"{question.get('question', '')}\n")
            choices = question.get('choices', [])

            for j, choice in enumerate(choices, 1):
                print(f"{j}. {choice}")

            # Start timer
            start_time = time.time()
            print(f"\nTime limit: {time_limit} seconds")

            # Get user answer
            user_answer = None
            timed_out = False

            while True:
                elapsed = time.time() - start_time
                remaining = max(0, time_limit - elapsed)

                if remaining <= 0:
                    timed_out = True
                    break

                try:
                    # Show countdown
                    print(f"\rTime remaining: {remaining:.1f}s ", end='', flush=True)

                    # Simple timeout mechanism (not perfect but functional)
                    answer_input = input("\nYour answer: ").strip()

                    # Check if time is up
                    if time.time() - start_time > time_limit:
                        timed_out = True
                        break

                    answer_num = int(answer_input)

                    if 1 <= answer_num <= len(choices):
                        user_answer = choices[answer_num - 1]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(choices)}")
                except ValueError:
                    print("Please enter a valid number")
                except (KeyboardInterrupt, EOFError):
                    break

            total += 1
            difficulty = question.get('difficulty', 'easy')

            if timed_out:
                print(f"\n\n⏰ {get_wrong_answer_message()} Time's up!")
                print(f"Correct answer: {question.get('answer', '')}")
                tracker.record_answer(course.name, question.get('lesson', 'Unknown'),
                                    question.get('question', ''), False, difficulty, 'Timed')
            else:
                # Check answer
                correct_answer = question.get('answer', '')
                time_taken = time.time() - start_time
                is_correct = user_answer == correct_answer

                xp_earned, leveled_up = tracker.record_answer(
                    course.name, question.get('lesson', 'Unknown'),
                    question.get('question', ''), is_correct, difficulty, 'Timed'
                )

                if is_correct:
                    correct += 1
                    total_xp_earned += xp_earned
                    print(f"\n✓ {get_correct_answer_message()} ({time_taken:.1f}s) +{xp_earned} XP")
                    if leveled_up:
                        print(f"{get_level_up_message()}")
                else:
                    print(f"\n✗ {get_wrong_answer_message()}")
                    print(f"Correct answer: {correct_answer}")

            input("\nPress Enter for next question...")

        # Record session
        duration = int(time.time() - session_start)
        tracker.record_session(course.name, 'Timed Challenge', correct, total, duration)

        # Show final score
        clear_screen()
        print_header("CHALLENGE COMPLETE")
        print_score(correct, total)
        print(f"💰 Total XP Earned: {total_xp_earned}\n")

        # Performance feedback
        percentage = (correct / total * 100) if total > 0 else 0
        if percentage >= 80:
            print("⚡ Incredible! You're lightning fast AND accurate!")
        elif percentage >= 60:
            print("🏃 Great job under pressure!")
        else:
            print("💪 Keep practicing! Speed comes with familiarity.")

        input("\nPress Enter to continue...")
