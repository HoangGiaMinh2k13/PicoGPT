import random

def make_dataset(filename="data/dataset.txt", num_lines=10000):
    lines = []

    # --- Conversation patterns ---
    conversations = [
        ("Hello!", "Hi there!"),
        ("How are you?", "I am fine, thank you."),
        ("What is your name?", "I am PicoGPT."),
        ("Are you smart?", "I try my best."),
        ("Do you like music?", "Yes, I enjoy simple melodies."),
        ("Goodbye!", "See you later!")
    ]

    # --- Facts ---
    facts = [
        "The Earth orbits the Sun.",
        "Water boils at 100 degrees Celsius.",
        "The Moon has no atmosphere.",
        "The capital of France is Paris.",
        "The human heart has four chambers.",
        "The brain has billions of neurons.",
        "The sky looks blue because of scattering.",
        "The apple is red.",
        "The trees and grass is green.",
        "The banana is yellow.",
        "The Sun rises in the East.",
        "The Sun sets in the West"
    ]

    # --- Science ---
    science = [
        "Hydrogen is the first element in the periodic table.",
        "The speed of light is about 300,000 kilometers per second.",
        "Gravity pulls objects toward the Earth.",
        "Energy equals mass times the speed of light squared.",
        "The Milky Way is a galaxy."
    ]

    # --- Math equations ---
    math_lines = []
    for a in range(1, 51):
        for b in range(1, 51):
            math_lines.append(f"{a} + {b} = {a+b}")
            math_lines.append(f"{a} - {b} = {a-b}")
            math_lines.append(f"{a} x {b} = {a*b}")

    # --- Stories ---
    stories = [
        "The cat chased the mouse across the field.",
        "The dog barked at the moon all night.",
        "The mouse eats cheese all day.",
        "The cows give milk and moo."
    ]

    # --- Philosophy ---
    philosophy = [
        "There is no definite meaning of life.",
        "Truth is a pathless land.",
        "Become what you are."
    ]

    # --- Build dataset ---
    all_categories = [facts, science, stories, philosophy]
    for _ in range(num_lines):
        category = random.choice(all_categories)
        if category == facts:
            lines.append(random.choice(facts))
        elif category == science:
            lines.append(random.choice(science))
        elif category == stories:
            lines.append(random.choice(stories))
        elif category == philosophy:
            lines.append(random.choice(philosophy))

        # sprinkle conversations
        if random.random() < 0.05:
            u, b = random.choice(conversations)
            lines.append(f"USER: {u}\nBOT: {b}")

        # sprinkle math
        if random.random() < 0.2:
            lines.append(random.choice(math_lines))

    # --- Save file ---
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Wrote {len(lines)} lines to {filename}")


if __name__ == "__main__":
    make_dataset()
