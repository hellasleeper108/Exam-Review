"""Progress tracking, XP system, and leaderboard functionality."""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class ProgressTracker:
    """Tracks user progress, XP, and achievements."""

    def __init__(self, data_file: str = "user_progress.json"):
        self.data_file = Path.home() / ".exam_review" / data_file
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load progress data from JSON file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._create_new_profile()
        return self._create_new_profile()

    def _create_new_profile(self) -> Dict:
        """Create a new user profile."""
        return {
            "username": "Player",
            "total_xp": 0,
            "level": 1,
            "courses": {},
            "sessions": [],
            "achievements": [],
            "created_at": datetime.now().isoformat()
        }

    def _save_data(self):
        """Save progress data to JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save progress: {e}")

    def get_xp_for_difficulty(self, difficulty: str) -> int:
        """Calculate XP based on difficulty."""
        xp_map = {
            "easy": 10,
            "medium": 25,
            "hard": 50
        }
        return xp_map.get(difficulty, 10)

    def calculate_level(self, total_xp: int) -> int:
        """Calculate level based on total XP (exponential curve)."""
        # Level = sqrt(XP / 100)
        import math
        return max(1, int(math.sqrt(total_xp / 100)) + 1)

    def xp_for_next_level(self, current_level: int) -> int:
        """Calculate XP needed for next level."""
        return ((current_level) ** 2) * 100

    def award_xp(self, amount: int):
        """Award XP and check for level up."""
        old_level = self.data["level"]
        self.data["total_xp"] += amount
        new_level = self.calculate_level(self.data["total_xp"])

        self.data["level"] = new_level
        self._save_data()

        return new_level > old_level  # True if leveled up

    def record_answer(self, course_name: str, lesson: str, question: str,
                     correct: bool, difficulty: str, mode: str):
        """Record a question answer and award XP."""
        # Initialize course if not exists
        if course_name not in self.data["courses"]:
            self.data["courses"][course_name] = {
                "questions_answered": 0,
                "correct_answers": 0,
                "xp_earned": 0,
                "modes_played": {},
                "lessons_completed": []
            }

        course = self.data["courses"][course_name]
        course["questions_answered"] += 1

        if correct:
            course["correct_answers"] += 1
            xp = self.get_xp_for_difficulty(difficulty)
            course["xp_earned"] += xp
            leveled_up = self.award_xp(xp)
            return xp, leveled_up

        return 0, False

    def record_session(self, course_name: str, mode: str,
                      correct: int, total: int, duration_seconds: int = 0):
        """Record a completed game session."""
        session = {
            "course": course_name,
            "mode": mode,
            "correct": correct,
            "total": total,
            "accuracy": round((correct / total * 100) if total > 0 else 0, 1),
            "duration": duration_seconds,
            "timestamp": datetime.now().isoformat()
        }

        self.data["sessions"].append(session)

        # Track mode stats
        if course_name in self.data["courses"]:
            modes = self.data["courses"][course_name].setdefault("modes_played", {})
            if mode not in modes:
                modes[mode] = {"sessions": 0, "total_correct": 0, "total_questions": 0}

            modes[mode]["sessions"] += 1
            modes[mode]["total_correct"] += correct
            modes[mode]["total_questions"] += total

        self._save_data()

    def get_stats(self) -> Dict[str, Any]:
        """Get overall statistics."""
        total_questions = sum(
            c["questions_answered"]
            for c in self.data["courses"].values()
        )
        total_correct = sum(
            c["correct_answers"]
            for c in self.data["courses"].values()
        )

        accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0

        return {
            "username": self.data["username"],
            "level": self.data["level"],
            "total_xp": self.data["total_xp"],
            "xp_to_next": self.xp_for_next_level(self.data["level"]) - self.data["total_xp"],
            "total_questions": total_questions,
            "total_correct": total_correct,
            "accuracy": round(accuracy, 1),
            "courses_played": len(self.data["courses"]),
            "total_sessions": len(self.data["sessions"])
        }

    def get_course_stats(self, course_name: str) -> Dict[str, Any]:
        """Get statistics for a specific course."""
        if course_name not in self.data["courses"]:
            return None

        course = self.data["courses"][course_name]
        accuracy = (course["correct_answers"] / course["questions_answered"] * 100) \
                   if course["questions_answered"] > 0 else 0

        return {
            "course": course_name,
            "questions_answered": course["questions_answered"],
            "correct_answers": course["correct_answers"],
            "accuracy": round(accuracy, 1),
            "xp_earned": course["xp_earned"],
            "modes_played": course.get("modes_played", {})
        }

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Get leaderboard by course performance."""
        leaderboard = []

        for course_name, course_data in self.data["courses"].items():
            if course_data["questions_answered"] > 0:
                accuracy = (course_data["correct_answers"] /
                           course_data["questions_answered"] * 100)

                leaderboard.append({
                    "course": course_name,
                    "xp": course_data["xp_earned"],
                    "correct": course_data["correct_answers"],
                    "total": course_data["questions_answered"],
                    "accuracy": round(accuracy, 1)
                })

        # Sort by XP earned
        leaderboard.sort(key=lambda x: x["xp"], reverse=True)
        return leaderboard

    def set_username(self, username: str):
        """Set or update username."""
        self.data["username"] = username
        self._save_data()

    def display_stats(self):
        """Display formatted statistics."""
        stats = self.get_stats()

        print("\n" + "=" * 60)
        print(f"PLAYER STATS - {stats['username']}")
        print("=" * 60)
        print(f"Level: {stats['level']}")
        print(f"Total XP: {stats['total_xp']} ({stats['xp_to_next']} XP to next level)")
        print(f"Questions Answered: {stats['total_questions']}")
        print(f"Correct Answers: {stats['total_correct']}")
        print(f"Overall Accuracy: {stats['accuracy']}%")
        print(f"Courses Played: {stats['courses_played']}")
        print(f"Total Sessions: {stats['total_sessions']}")
        print("=" * 60 + "\n")

    def display_leaderboard(self):
        """Display course leaderboard."""
        leaderboard = self.get_leaderboard()

        if not leaderboard:
            print("\nNo courses played yet! Start playing to build your leaderboard.\n")
            return

        print("\n" + "=" * 70)
        print("COURSE LEADERBOARD - Top Performances")
        print("=" * 70)
        print(f"{'Rank':<6} {'Course':<30} {'XP':<8} {'Score':<15} {'Accuracy':<10}")
        print("-" * 70)

        for i, entry in enumerate(leaderboard[:10], 1):  # Top 10
            course_display = entry['course'][:28] + ".." if len(entry['course']) > 30 else entry['course']
            score_display = f"{entry['correct']}/{entry['total']}"

            print(f"{i:<6} {course_display:<30} {entry['xp']:<8} "
                  f"{score_display:<15} {entry['accuracy']}%")

        print("=" * 70 + "\n")

    def display_progress_bar(self):
        """Display XP progress bar to next level."""
        stats = self.get_stats()
        current_level_xp = (stats['level'] - 1) ** 2 * 100
        xp_in_level = stats['total_xp'] - current_level_xp
        xp_needed = self.xp_for_next_level(stats['level']) - stats['total_xp']
        total_for_level = xp_in_level + xp_needed

        progress = xp_in_level / total_for_level if total_for_level > 0 else 0
        bar_length = 30
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"\nLevel {stats['level']} [{bar}] Level {stats['level'] + 1}")
        print(f"{xp_in_level} / {total_for_level} XP ({xp_needed} XP to go)\n")
