"""Base class for all game modes."""

from abc import ABC, abstractmethod
from utils.course_loader import Course


class GameMode(ABC):
    """Abstract base class for game modes."""

    @abstractmethod
    def play(self, course: Course):
        """
        Main game loop for this mode.

        Args:
            course: The Course object containing questions and lessons
        """
        pass

    def get_user_input(self, prompt: str, valid_options: list = None) -> str:
        """
        Get validated user input.

        Args:
            prompt: The prompt to display
            valid_options: List of valid options (case-insensitive), or None for any input

        Returns:
            User's input (lowercased if valid_options provided)
        """
        while True:
            user_input = input(prompt).strip()

            if valid_options is None:
                return user_input

            if user_input.lower() in [opt.lower() for opt in valid_options]:
                return user_input.lower()

            print(f"Please enter one of: {', '.join(valid_options)}")
