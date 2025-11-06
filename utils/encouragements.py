"""Random encouragement messages for wrong answers and achievements."""

import random

# Funny/encouraging messages for wrong answers
WRONG_ANSWER_MESSAGES = [
    "Close enough for government work!",
    "Well, that's one way to do it...",
    "You miss 100% of the shots you don't take. This was one of them.",
    "Not quite, but I like your confidence!",
    "Swing and a miss! But hey, Babe Ruth struck out too.",
    "That's... creative thinking!",
    "Your answer was in the neighborhood. Wrong neighborhood, but still.",
    "Plot twist: that wasn't it!",
    "Nice try! The universe just had other plans.",
    "Incorrect, but with style!",
    "So close! If this were horseshoes or hand grenades...",
    "Bold choice! Wrong, but bold.",
    "Not the answer we were looking for, but we appreciate the enthusiasm!",
    "Ooh, you were in the ballpark. Unfortunately, it's a big ballpark.",
    "That's definitely... an answer!",
    "Better luck next time, champ!",
    "The computer says no.",
    "Error 404: Correct answer not found.",
    "You've discovered a new wrong answer! Achievement unlocked?",
    "At least you're consistent... consistently wrong on that one!",
    "That's one for the blooper reel!",
    "Narrator: It was not, in fact, the right answer.",
    "Your confidence was 10/10. Your accuracy was... not.",
    "Good hustle out there!",
    "Well, you definitely picked SOMETHING!",
]

# Encouraging messages for correct answers
CORRECT_ANSWER_MESSAGES = [
    "Nailed it!",
    "You're on fire!",
    "Boom! Correct!",
    "That's what I'm talking about!",
    "Look at you, smarty pants!",
    "Absolutely crushed it!",
    "You're a natural!",
    "Knowledge bomb deployed!",
    "Chef's kiss! Perfect!",
    "Big brain energy right there!",
    "Somebody's been studying!",
    "Flawless victory!",
    "You make this look easy!",
    "Genius mode activated!",
    "Correctamundo!",
]

# Level up messages
LEVEL_UP_MESSAGES = [
    "🎉 LEVEL UP! You're ascending to new heights!",
    "⭐ LEVEL UP! Your brain just got bigger!",
    "🚀 LEVEL UP! Next stop: genius!",
    "🏆 LEVEL UP! You're unstoppable!",
    "✨ LEVEL UP! Knowledge overload in progress!",
    "💪 LEVEL UP! Your XP grind is paying off!",
    "🎊 LEVEL UP! You've unlocked a new tier of awesome!",
    "🔥 LEVEL UP! You're absolutely crushing it!",
]

# Streak messages
STREAK_MESSAGES = {
    3: "🔥 3 in a row! You're heating up!",
    5: "🔥🔥 5-streak! You're on fire!",
    7: "🔥🔥🔥 7-STREAK! UNSTOPPABLE!",
    10: "🔥🔥🔥🔥 10-STREAK! ARE YOU EVEN HUMAN?!",
}


def get_wrong_answer_message() -> str:
    """Get a random encouraging message for a wrong answer."""
    return random.choice(WRONG_ANSWER_MESSAGES)


def get_correct_answer_message() -> str:
    """Get a random encouraging message for a correct answer."""
    return random.choice(CORRECT_ANSWER_MESSAGES)


def get_level_up_message() -> str:
    """Get a random level up message."""
    return random.choice(LEVEL_UP_MESSAGES)


def get_streak_message(streak: int) -> str:
    """Get a message for achieving a streak milestone."""
    # Check for exact matches first
    if streak in STREAK_MESSAGES:
        return STREAK_MESSAGES[streak]

    # For streaks above 10, give periodic messages
    if streak > 10 and streak % 5 == 0:
        return f"🔥 {streak}-STREAK! Someone call the fire department!"

    return None
