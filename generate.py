from openai import OpenAI
import json
import time

def generate(situation: str, specific_examples: str, n_flashcards: int, language: str = "spanish", country: str = "Mexico", step_size=50):
    system_message = """You generate flashcards, as a JSON array, in the following format:

{
    "flashcards": {
        "front": string;
        "back": string;
        "explanation": string | null;
        "worksFromEitherSide": boolean;
        "level": "basic" | "intermediate" | "advanced";
    }[]
}

Do "explanation", if it's a whole sentence. Give individual translations for each word, and explaining grammar, if there's something special. If it's a singular word, leave it null.

Please generate around """ + str(step_size) + """ flashcards at a time."""

    user_message = f"""Hi. Here's the situation:

I need to go to {situation} in {language} in {country}.

I currently know ZERO {language}.

Please generate a bunch of Anki Flashcards for me, going from most basic thing I might have to say at the event ("Hi, what's your name? My name is Louis"), all the way to the higher concepts, specific to the setting ({specific_examples})

Focus on SENTENCES not words."""

    print("\n\nsystem:", system_message)
    print("\n\n\n")
    print("\n\nuser:", user_message)

    client = OpenAI()
    messages = [{
        "role": "system",
        "content": system_message
    }, {
        "role": "user",
        "content": user_message
    }]
    flashcards = []
    
    while len(flashcards) < n_flashcards:
        try:
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                # model="gpt-3.5-turbo-1106",
                messages=messages,
                response_format={"type": "json_object"},
                max_tokens=4096,
            )
        except Exception as e:
            print("Error", e)
            print("Error. Ending...")
            break
        messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        message_flashcards = json.loads(response.choices[0].message.content)["flashcards"]
        print("Added", len(message_flashcards), "flashcards.")
        flashcards += message_flashcards
        json.dump(flashcards, open("debug.json", "w"), indent=4)
    
    flashcards_filename = "flashcards-" + str(int(time.time())) + ".json"
    json.dump(flashcards, open(flashcards_filename, "w"), indent=4)

if __name__ == "__main__":
    generate(
        situation="a consciousness conference",
        specific_examples="I am building a meditation app, What's your background in qualia, etc.",
        n_flashcards=400
    )