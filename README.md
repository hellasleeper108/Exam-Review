# Exam Review Game

An interactive CLI-based exam review application with multiple game modes to help you study effectively!

## Features

### Game Modes

1. **Flashcards** - Review concepts at your own pace
   - Self-paced review
   - Show/hide answers
   - Perfect for initial learning

2. **Multiple Choice Quiz** - Test your knowledge
   - Immediate feedback
   - Explanations for each answer
   - Track your score

3. **Timed Challenge** - Race against the clock!
   - 30 seconds per question
   - Fast-paced learning
   - Builds quick recall

4. **Sudden Death** - One mistake and you're out!
   - High stakes mode
   - Build your streak
   - For the brave and masochistic

### Course System

- Courses are stored as JSON files in the `courses/` directory
- Each course contains:
  - Lesson titles and descriptions
  - Question pools with multiple types
  - Difficulty levels (easy, medium, hard)
  - Detailed explanations

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd Exam-Review
   ```

2. Make the scripts executable:
   ```bash
   chmod +x review.py exam_game.sh
   ```

3. Ensure Python 3 is installed:
   ```bash
   python3 --version
   ```

## Usage

### Run the application

Option 1 - Using Python directly:
```bash
python3 review.py
```

Option 2 - Using the shell wrapper:
```bash
./exam_game.sh
```

### Navigate the menus

1. Select a course from the available courses
2. Choose your game mode
3. Answer questions and learn!
4. Return to menu or exit when done

## Creating Custom Courses

Create a new JSON file in the `courses/` directory with the following structure:

```json
{
  "name": "Your Course Name",
  "description": "Course description",
  "lessons": [
    {
      "title": "Lesson Title",
      "description": "Lesson description"
    }
  ],
  "questions": [
    {
      "question": "What is the question?",
      "type": "multiple_choice",
      "choices": [
        "Option 1",
        "Option 2",
        "Option 3",
        "Option 4"
      ],
      "answer": "Option 1",
      "explanation": "Why this is the correct answer",
      "lesson": "Lesson Title",
      "difficulty": "easy"
    },
    {
      "question": "Flashcard question?",
      "type": "flashcard",
      "answer": "The answer",
      "explanation": "Additional context",
      "lesson": "Lesson Title",
      "difficulty": "medium"
    }
  ]
}
```

### Question Types

- **multiple_choice**: Questions with multiple options (used in Quiz, Timed, and Sudden Death modes)
- **flashcard**: Questions with free-form answers (used in Flashcard mode)

### Difficulty Levels

- **easy**: Fundamental concepts
- **medium**: Intermediate knowledge
- **hard**: Advanced topics

## Project Structure

```
Exam-Review/
├── review.py              # Main entry point
├── exam_game.sh          # Shell script wrapper
├── courses/              # Course JSON files
│   ├── cs101.json
│   ├── psyc100.json
│   ├── py101.json
│   ├── python_basics.json
│   └── web_development.json
├── game_modes/           # Game mode implementations
│   ├── __init__.py
│   ├── base.py
│   ├── flashcards.py
│   ├── quiz.py
│   ├── timed.py
│   └── sudden_death.py
└── utils/                # Utility modules
    ├── __init__.py
    ├── course_loader.py
    └── display.py
```

## Courses Included

### Comprehensive Courses (Lesson-by-Lesson Coverage)
- **PY101 Comprehensive**: All 52 lessons with 3-4 questions each - **180 questions total**
  - Week 1: Printing, variables, operators, functions, strings, scope, f-strings, debugging
  - Week 2: Control flow, if/else, logical operators, loops, range, lists, sorting
  - Week 3: String methods, split/join, dictionaries, nested structures, parsing, counting

- **CS101 Comprehensive**: All 44 lessons with 3-4 questions each - **154 questions total**
  - Week 4: Naming, docstrings, clean code, refactoring, testing, debugging
  - Week 5: Planning, pseudocode, patterns, stubs, incremental development, dry running
  - Week 6: Problem statements, decomposition, prioritization, pipelines

- **PSYC100 Comprehensive**: All 33 lessons with 3-4 questions each - **119 questions total**
  - Week 7: Social psychology (obedience, conformity, bystander effect, cognitive dissonance)
  - Week 8: Professional success (Maslow, SDT, goal-setting, growth mindset, flow, grit)
  - Week 9: Cognitive biases (heuristics, anchoring, framing, Dunning-Kruger, false memory)

### Quick Review Courses
- **PY101 Quick Review**: Python fundamentals overview - 28 questions
- **CS101 Quick Review**: Professional practices overview - 28 questions
- **PSYC100 Quick Review**: Psychology concepts overview - 28 questions

### Example/Demo Courses
- **Python Basics**: Simple intro to variables, data types, functions, control flow - 8 questions
- **Web Development**: HTML, CSS, JavaScript fundamentals - 7 questions

## Tips for Effective Study

1. Start with **Flashcards** to learn new material
2. Use **Quiz Mode** to test your understanding
3. Challenge yourself with **Timed Mode** to build speed
4. Test your mastery with **Sudden Death** mode

## Requirements

- Python 3.6 or higher
- No external dependencies required!

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to add more courses, game modes, or features! Contributions are welcome.
