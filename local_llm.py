import re
import requests
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

API_URL = "http://127.0.0.1:5000"


def extract_letter(response_text):
    """
    Extract a valid single letter from the LLM's response.
    """
    import re
    match = re.search(r'\b[a-z]\b', response_text.lower())  # Match exactly one letter
    return match.group(0) if match else None

def get_next_best_guess(state):
    """
    Suggest the next best letter based on the current state of the game.
    Prioritize unguessed vowels first, then common consonants.
    """
    vowels = ['a', 'e', 'i', 'o', 'u']
    common_consonants = ['r', 's', 't', 'l', 'n']
    all_letters = vowels + common_consonants + list('bcdfghjkmnpqvwxyz')

    guessed_letters = set(state['guessed_letters'])
    for letter in all_letters:
        if letter not in guessed_letters:
            return letter
    return None


def play_hangman_with_llm():
    response = requests.get(f"{API_URL}/start")
    print(response.json()["message"])

    while True:
        response = requests.get(f"{API_URL}/state")
        state = response.json()

        if state.get("status") in ["won", "lost"]:
            print(f"Game Over! Status: {state['status']}")
            print(f"The word was: {state.get('word')}")

            provide_game_commentary(state)
            break

        print(f"Word: {state['word_display']}")
        print(f"Guessed Letters: {', '.join(state['guessed_letters'])}")
        print(f"Wrong Attempts: {state['wrong_guesses']}/{state['max_attempts']}")
        print("============================================================================================")

        model = OllamaLLM(model="mistral-nemo")
        prompt_template = (
            f"You are playing Hangman. The word so far is: {state['word_display']}.\n"
            f"The letters guessed so far are: {', '.join(state['guessed_letters'])}.\n"
            f"You have {state['max_attempts'] - state['wrong_guesses']} attempts left.\n"
            f"Your response should be a single lowercase letter with no explanation or additional text."
        )
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | model
        raw_response = chain.invoke({"input": ""}).strip()

        guessed_letter = extract_letter(raw_response)

        if not guessed_letter or guessed_letter in state['guessed_letters']:
            guessed_letter = get_next_best_guess(state)
            if guessed_letter:
                print(f"Fallback guess: {guessed_letter}")
            else:
                print("No valid guesses left. Exiting.")
                break

        try:
            guess_response = requests.post(f"{API_URL}/guess", json={"letter": guessed_letter})
            print(f"LLM guessed: {guessed_letter}")
            print(guess_response.json())
        except requests.exceptions.HTTPError as e:
            print(
                f"Error with LLM's guess: {guessed_letter}. Error: {e.response.json().get('detail', 'Unknown error')}")


def provide_game_commentary(state):
    """
    Use the LLM to generate a reflection or commentary about the game.
    """
    model = OllamaLLM(model="mistral-nemo")
    prompt_template = (
        f"The Hangman game has ended. Here is the summary:\n"
        f"Final word: {state.get('word')}\n"
        f"Reflect on the game. Was the strategy effective? Suggest ways to improve for the next game.\n"
        f"Your response should be a concise reflection, focusing on what went well and what can be improved."
    )
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | model
    commentary = chain.invoke({"input": ""}).strip()

    print("\nLLM's Post-Game Commentary:")
    print(commentary)


if __name__ == "__main__":
    play_hangman_with_llm()
