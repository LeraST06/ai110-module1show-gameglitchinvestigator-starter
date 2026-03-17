# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

When I just ran the game, it looked fine, but as I started playing, I noticed multiple glitches. The first bug I notices was that the hints were backwards. Another bug I notices was that the restart button was not working. Also, the attempts counter is not working properly either.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude on this project. For the correct suggestion: Claude identified and fixed multiple bugs: the backwards hints in `check_guess`, the attempts counter starting at 1 instead of 0, the New Game button not resetting game status, the double-press issue caused by Streamlit's form rerun behavior, invalid guesses counting as attempts, the score rewarding wrong guesses, and stale display values for history and attempts left. I verified each fix by playing the game and running pytest, and all tests passed. For the misleading suggestion: while fixing the stale display values, Claude added `st.rerun()` after each guess, which accidentally caused hints to stop showing after the first guess. I noticed this while playing and Claude then fixed it by storing the hint in `st.session_state` so it survived the rerun.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed when I could play through the game without the bad behavior happening. For pytest, Claude helped write tests in `tests/test_game_logic.py` targeting the specific bugs. For example, `test_too_high_hint_says_go_lower` checks that a guess above the secret returns a message containing "LOWER". I also caught bugs manually that tests couldn't easily cover, like the double-press issue and the hints disappearing, which I found by just playing the game after each change. Claude also pointed out that the existing starter tests were broken because they compared `check_guess` results to plain strings, but the function returns a tuple.

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing because `random.randint()` was called at the top of the script every time Streamlit reran the page — and Streamlit reruns the entire script on every user interaction like a button click. So each click generated a brand new secret number. Streamlit "reruns" are like refreshing the page from scratch every time you do anything; session state is a way to save values so they survive those refreshes. The fix was wrapping the secret generation in `if "secret" not in st.session_state`, so it only runs once at the start of a session and stays the same for the rest of the game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is asking AI to explain the bug and its cause before jumping straight to a fix — that way I actually understand what changed instead of just accepting code. Next time I would also ask for more in-depth comments in the code so I don't forget what each fix does later. Honestly, my view of AI-generated code hasn't changed much since I already use AI tools a lot, but this was my first time using Claude Code directly inside VS Code and it saved a huge amount of time — having it built into the editor instead of switching between tabs made the whole debugging process much faster.
