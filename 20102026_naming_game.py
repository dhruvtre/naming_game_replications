# Reproduction attempt from Sharp transition towards shared vocabularies in multi-agent systems
# Creating a naming game

n_agents_1 = 4
n_agents_2 = 50
n_agents_3 = 3000

import csv

object_list = ["object1", "object2", "object3", "object4", "object5"]
from itertools import count
word_counter = count(1)

def object_initialization(object_list):
    print("Enter the number of objects to initialize. Max 5")
    n_objects = input("Number of objects: ")
    return object_list[:int(n_objects)]

def agent_initialization(n_agents, n_objects, object_list):
    agents = []
    for i in range(n_agents):
        agent = {
            "id": i,
            "vocabulary": {obj: [] for obj in object_list[:n_objects]}
        }
        agents.append(agent)
    return agents

import random

def speaker_choice(agents):
    return random.choice(agents)

def listener_choice(agents, speaker):
    listeners = [agent for agent in agents if agent != speaker]
    return random.choice(listeners)

def object_choice(object_list):
    return random.choice(object_list)

def single_turn(speaker_agent, listener_agent, object_chosen, verbose=False):

    # accessing speaker vocab
    speaker_vocab = speaker_agent["vocabulary"]

    # accessing listener vocab
    listener_vocab = listener_agent["vocabulary"]

    # Both agents must have been initialized with the chosen object.
    if object_chosen not in speaker_vocab or object_chosen not in listener_vocab:
        raise ValueError(f"{object_chosen!r} must be initialized for both agents.")

    if verbose:
        print(f"\nSpeaker {speaker_agent['id']} -> Listener {listener_agent['id']} | Object: {object_chosen}")
        print(f"Before: speaker={speaker_vocab[object_chosen]}, listener={listener_vocab[object_chosen]}")

    # checking if object exists in speaker vocab
    if object_chosen in speaker_vocab:
        # checking if word for object exists in speaker vocab
        if speaker_vocab[object_chosen]:
            word = random.choice(speaker_vocab[object_chosen])
        else:
            # initializing a new word for the object if it doesn't exist
            word = f"word_{next(word_counter)}"
            speaker_vocab[object_chosen].append(word)
            if verbose:
                print(f"Invented: {word}")
    else:
        print("Object not found in speaker's vocabulary.")

    if verbose:
        print(f"Spoken word: {word}")

    # checking if the chosen object exists in listener vocab
    if object_chosen in listener_vocab: 
        # checking if word for chosen object exists in listener vocab
        if word in listener_vocab[object_chosen]:
            if verbose:
                print("Success! The listener understood the speaker.")
            success = True
            # Updating the vocab with the common word only
            speaker_vocab[object_chosen] = [word]
            listener_vocab[object_chosen] = [word]
        else:
            if verbose:
                print("Failure! The listener did not understand the speaker.")
                print("New word appended to listener vocabulary for chosen object.")
            listener_vocab[object_chosen].append(word)
            success = False
    else:
        print("Object not found in listener's vocabulary.")

    if verbose:
        print(f"After:  speaker={speaker_vocab[object_chosen]}, listener={listener_vocab[object_chosen]}")

    # Calculating single turn metrics
    speaker_vocab_length = len(speaker_vocab[object_chosen])
    listener_vocab_length = len(listener_vocab[object_chosen])
    unique_simulation_vocab = len(set(speaker_vocab[object_chosen] + listener_vocab[object_chosen]))
    return speaker_vocab_length, listener_vocab_length, unique_simulation_vocab, success


def main():
    random.seed(45)  # Makes fresh runs repeatable while debugging

    selected_objects = object_initialization(object_list)
    n_agents = input("Enter the number of agents to initialize: ")
    n_turns = input("Enter the number of turns to simulate: ")

    agents = agent_initialization(
        int(n_agents),
        len(selected_objects),
        selected_objects
    )
    
    verbose = False
    turn_metrics = []
    filename = f"run_004_{n_turns}t_{n_agents}a_{len(selected_objects)}o_s45.csv"
    for turn_number in range(1, int(n_turns) + 1):
        if verbose:
            print(f"\n--- Turn {turn_number} ---")

        speaker = speaker_choice(agents)
        listener = listener_choice(agents, speaker)
        chosen_object = object_choice(selected_objects)

        speaker_vocab_length, listener_vocab_length, unique_vocab, success = single_turn(speaker, listener, chosen_object, verbose=verbose)

        all_words = [
            word
            for agent in agents
            for word in agent["vocabulary"][chosen_object]
        ]

        total_words = len(all_words)
        distinct_words = len(set(all_words))
        print(f"Population wide total words at the end of turn {turn_number}: {total_words}, Distinct words: {distinct_words}")


        # saving turn metrics
        turn_metrics.append({
            "turn": turn_number,
            "speaker_id": speaker["id"],
            "listener_id": listener["id"],
            "object": chosen_object,
            "speaker_vocab_length": speaker_vocab_length,
            "listener_vocab_length": listener_vocab_length,
            "unique_simulation_vocab": unique_vocab,
            "population_total_words": total_words,
            "population_distinct_words": distinct_words,
            "success": success
        })

    with open(filename, "x", newline="", encoding="utf-8") as csv_file:
            columns = turn_metrics[0].keys()

            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(turn_metrics)

    print(f"Saved {len(turn_metrics)} turns to {filename}")
    if verbose:
        print("\n--- Final vocabularies ---")
        for agent in agents:
            print(f"Agent {agent['id']}: {agent['vocabulary']}")


if __name__ == "__main__":
    main()
