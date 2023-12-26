import genanki
import json
import random

def create_deck(filename, deck_name="Custom Deck"):
    data = json.load(open(filename, "r"))

    deck = genanki.Deck(
        random.randint(1, 1e9),
        deck_name
    )
    
    # Define a simple model
    my_model = genanki.Model(
        random.randint(1, 1e9),
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])

    # Add cards to the deck
    for item in data:
        front = item["front"]
        back = item["back"]
        explanation = ""
        if item["explanation"]:
            explanation = "<br><br>" + item["explanation"]
        
        note = genanki.Note(
            model=my_model,
            fields=[front, back + explanation]
        )
        deck.add_note(note)
        if item["worksFromEitherSide"]:
            reverse_note = genanki.Note(
                model=my_model,
                fields=[back, front + explanation]
            )
            deck.add_note(reverse_note)

    # Save the deck to a file
    genanki.Package(deck).write_to_file(f'{deck_name}.apkg')

if __name__ == "__main__":
    # Call the function with your data
    create_deck("1703622113.json", "My Custom Test Deck")
