from logic_utils import check_guess, parse_guess, update_score

# ── Existing starter tests (fixed to unpack the tuple check_guess returns) ──

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# ── Bug fix: backwards hints ─────────────────────────────────────────────────

def test_too_high_hint_says_go_lower():
    # Bug was: guess > secret showed "Go HIGHER!" instead of "Go LOWER!"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    # Bug was: guess < secret showed "Go LOWER!" instead of "Go HIGHER!"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

# ── Bug fix: attempts counter starts at 0 ────────────────────────────────────

def test_first_win_score_uses_attempt_1():
    # With attempts starting at 0 and incrementing before check, first real
    # guess is attempt 1. Score should be 100 - 10*(1+1) = 80, not 70.
    score = update_score(0, "Win", attempt_number=1)
    assert score == 80

# ── parse_guess sanity checks ────────────────────────────────────────────────

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert err == "Enter a guess."

def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err == "That is not a number."
