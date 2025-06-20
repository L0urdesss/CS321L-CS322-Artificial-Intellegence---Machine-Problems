import time

names = {"P": "Person",
         "F": "Fox",
         "C": "Chicken",
         "G": "Grain"}

forbidden_states = [{"F", "C"}, {"C", "G"}, {"F", "C", "G"}]


def story_intro():
    lines = [
        "Once upon a time, in a small village near a river, there lived a clever person with a fox, a chicken, "
        "and a sack of grain.",
        "One day, the person needed to transport these three items across the river.",
        "However, there was a small wooden boat that could only carry the person and one item at a time.",
        "The challenge was that if left alone, the fox would eat the chicken, and the chicken would eat the grain.",
        "The person needed to figure out how to transport all three items to the other side of the river without any "
        "harm.\n"
    ]

    for line in lines:
        print(line)
        time.sleep(2)


def print_state(state, move_count):
    left_bank, right_bank = state
    print("                  CURRENT STATE                    ")
    left_bank_display = [names[item] for item in left_bank]
    right_bank_display = [names[item] for item in right_bank]

    print(f"{left_bank_display} | RIVER | {right_bank_display if right_bank else '[]'}")
    print(f"Moves: {move_count}\n")


def get_move():
    print("Which item do you wish to take across the river?")
    answer = ""
    while answer.upper() not in ["P", "F", "C", "G"]:
        answer = input("Just Person (P), Fox (F), Chicken (C) or Grain (G)? ")

    return answer.upper()


def process_move(move, state, move_count):
    temp_state = [state[0].copy(), state[1].copy()]
    containing_set = 0 if move in state[0] else 1
    if "P" not in state[containing_set]:
        print("\n\nNot allowed - the person must accompany the item.\n")
        print("")
        return state, move_count
    if containing_set == 0:
        temp_state[0].difference_update({move, "P"})
        temp_state[1].update([move, "P"])
    elif containing_set == 1:
        temp_state[1].difference_update({move, "P"})
        temp_state[0].update([move, "P"])
    if temp_state[0] not in forbidden_states and temp_state[1] not in forbidden_states:
        state = [temp_state[0].copy(), temp_state[1].copy()]
        move_count += 1
    else:
        print("\n\nNot allowed - one of your items would be eaten!\n")
    print("")
    return state, move_count


def is_win(state):
    return state[1] == {"P", "F", "C", "G"}


def main():
    print("\nPERSON, FOX, CHICKEN, AND GRAIN PROBLEM")

    while True:
        print("\n   MENU:   ")
        print("1. Solve the Problem")
        print("2. Display Least Moves Solution")
        print("3. Quit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            story_intro()
            left_bank = {"P", "F", "C", "G"}
            right_bank = set()
            state = [left_bank, right_bank]
            move_count = 0

            while not is_win(state):
                print_state(state, move_count)
                move = get_move()
                state, move_count = process_move(move, state, move_count)

            print_state(state, move_count)
            print("Well done - you solved the problem!")

            decision = input("\nDo you want to:\n1. Go back to the main menu\n2. Exit the program\nEnter your choice "
                             "(1/2): ")
            if decision == "1":
                continue
            elif decision == "2":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Going back to the main menu.")

        elif choice == "2":

            print("\nHere is the least possible moves for this problem")

            initial_state = ({"P", "F", "C", "G"}, set())

            moves = ["C", "P", "G", "C", "F", "P", "C"]

            print("\nCurrent State")

            print(
                f"{list(names[item] for item in initial_state[0])} | RIVER | {list(names[item] for item in initial_state[1])}\n")

            move_count = 0

            state = list(initial_state)

            for move in moves:
                move_count += 1

                print(f"Which item do you wish to take across the river?")

                print(f"Just Person(P), Fox(F), Chicken(C) or Grain(G)")

                print(f"Enter: {move}\n")

                state, _ = process_move(move, state, move_count)

                print(f"Current State")

                print(
                    f"{list(names[item] for item in state[0])} | RIVER | {list(names[item] for item in state[1])}")

                print(f"Moves: {move_count}\n")

            print("\n                 FINAL STATE                  ")

            print("[] | RIVER | ['Fox', 'Grain', 'Chicken', 'Person']")

            print(f"Moves: {move_count}\n")

            input("Press enter to go back to the main\n")

        elif choice == "3":
            print("\nExiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
