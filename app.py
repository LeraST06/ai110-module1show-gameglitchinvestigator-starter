import random
import streamlit as st
# FIX: Refactored all game logic functions out of app.py into logic_utils.py
# using Claude Agent mode, which also moved the imports here.
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: attempts initialized to 0 (was 1), fixing the off-by-one in attempts left.
# Identified by me, corrected with Claude.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: last_hint persists the hint message across reruns so st.rerun() doesn't
# wipe it. Diagnosed and implemented with Claude.
if "last_hint" not in st.session_state:
    st.session_state.last_hint = None

# FIX: game_count key forces text input to reset when New Game is pressed.
# Claude suggested the dynamic key pattern.
if "game_count" not in st.session_state:
    st.session_state.game_count = 0

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIXME: Text input blur triggered a rerun (submit=False) before the button
# click rerun (submit=True), so every guess from the 2nd onward needed two
# presses. Fixed by wrapping input + submit in st.form to batch them as one event.
# FIX: Wrapped input and buttons in st.form — Claude explained the blur/rerun
# race condition and suggested the form pattern to fix it.
show_hint = st.checkbox("Show hint", value=True, key="show_hint")

# FIXME: st.rerun() cleared the hint before it could display. Fixed by storing
# the hint in session state so it persists across the rerun.
if show_hint and st.session_state.last_hint:
    st.warning(st.session_state.last_hint)

with st.form("guess_form"):
    raw_guess = st.text_input("Enter your guess:", key=f"guess_{st.session_state.game_count}")
    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Submit Guess 🚀")
    with col2:
        new_game = st.form_submit_button("New Game 🔁")

# FIXME: New Game button did not reset status, score, history, or hint —
# leaving the game stuck after a win or loss.
# FIX: Reset all session state fields on New Game. I spotted the missing fields;
# Claude helped reset them all cleanly including last_hint and game_count.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_hint = None
    st.session_state.game_count += 1
    st.success("New game started.")
    st.rerun()

# FIXME: Game never ended on a correct guess — missing st.rerun() after setting
# status, and end-game messages were only in the submit block (not shown after rerun).
# FIX: End-game messages moved to the status block and st.stop() used instead of
# st.rerun(). Claude identified the render-cycle issue causing this.
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.balloons()
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score} — Start a new game to play again."
        )
    else:
        st.error(
            f"Out of attempts! The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score} — Start a new game to try again."
        )
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        # FIXME: attempts incremented before input was validated, so typos and
        # empty submissions wasted an attempt. Now only valid guesses count.
        # FIX: Moved attempts increment inside the valid-guess branch. I noticed
        # the bug; Claude helped move the increment to the right place.
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)

        st.session_state.last_hint = message

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        # FIXME: st.rerun() after a win/loss wiped the render before the status
        # block could fire, requiring a second button press.
        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score} — Start a new game to play again."
            )
            st.stop()
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score} — Start a new game to try again."
                )
                st.stop()
            else:
                # FIXME: History, score, and attempts left all showed stale values
                # because display elements render before submit processing. A rerun
                # after each normal guess forces the page to reflect updated state.
                # FIX: Added st.rerun() after normal guesses. Claude explained why
                # Streamlit renders top-to-bottom before submit logic runs.
                st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
