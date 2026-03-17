def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIXME: Hints were backwards — "Go HIGHER!" showed when guess was too high.
    # FIX: Swapped the hint messages so they match the correct direction.
    # I identified the bug by playing the game; Claude confirmed the fix in check_guess.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIXME: "Too High" on even attempts gave +5 points, rewarding a wrong guess.
    # FIX: Removed the even/odd branch — all wrong guesses deduct 5 consistently.
    # FIXME: Score had no floor and could go negative.
    # FIX: Added max(0, ...) so score never drops below 0.
    # Both fixes done with Claude after I noticed the scoring felt wrong during play.
    if outcome == "Too High":
        return max(0, current_score - 5)

    if outcome == "Too Low":
        return max(0, current_score - 5)

    return current_score
