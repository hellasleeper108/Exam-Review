"""Course loading and management utilities."""

import json
from pathlib import Path
from typing import List, Dict, Any


class Course:
    """Represents a course with lessons and questions."""

    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("name", "Unknown Course")
        self.description = data.get("description", "")
        self.lessons = data.get("lessons", [])
        self.questions = data.get("questions", [])

    def get_questions(self, difficulty: str = None, lesson: str = None) -> List[Dict]:
        """Filter questions by difficulty and/or lesson."""
        filtered = self.questions

        if difficulty:
            filtered = [q for q in filtered if q.get("difficulty") == difficulty]

        if lesson:
            filtered = [q for q in filtered if q.get("lesson") == lesson]

        return filtered

    def get_lesson_titles(self) -> List[str]:
        """Get list of lesson titles."""
        return [lesson.get("title", "") for lesson in self.lessons]


class CourseLoader:
    """Handles loading courses from JSON files."""

    def __init__(self, courses_dir: Path):
        self.courses_dir = Path(courses_dir)
        if not self.courses_dir.exists():
            self.courses_dir.mkdir(parents=True, exist_ok=True)

    def get_available_courses(self) -> List[str]:
        """Return list of available course files."""
        if not self.courses_dir.exists():
            return []

        return sorted([
            f.name for f in self.courses_dir.iterdir()
            if f.suffix == ".json"
        ])

    def load_course(self, filename: str) -> Course:
        """Load a course from a JSON file."""
        filepath = self.courses_dir / filename

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return Course(data)
