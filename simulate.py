import random
import pandas as pd
from datetime import datetime

def generate_euromillions():
    """Generate a random draw."""
    # Generate 5 unique numbers between 1 and 50
    numbers = random.sample(range(1, 51), 5)
    numbers.sort()

    # Generate 2 unique lucky stars between 1 and 12
    lucky_stars = random.sample(range(1, 13), 2)
    lucky_stars.sort()

    return numbers, lucky_stars

def compare_results(draw, ticket):
    """Compare the draw with the ticket and return the number of matching numbers and stars."""
    draw_numbers, draw_stars = draw
    ticket_numbers, ticket_stars = ticket

    # Calculate the number of matching numbers and stars
    matching_numbers = len(set(draw_numbers).intersection(ticket_numbers))
    matching_stars = len(set(draw_stars).intersection(ticket_stars))

    return matching_numbers, matching_stars


def get_fixed_combination():
    """Get a fixed Euromillions combination from the user."""
    while True:
        try:
            numbers = list(map(int, input("Enter 5 unique numbers between 1 and 50, separated by commas: ").split(",")))
            stars = list(
                map(int, input("Enter 2 unique lucky stars between 1 and 12, separated by commas: ").split(",")))

            if len(numbers) == 5 and len(stars) == 2 and \
                    all(1 <= num <= 50 for num in numbers) and \
                    all(1 <= star <= 12 for star in stars) and \
                    len(set(numbers)) == 5 and len(set(stars)) == 2:
                return sorted(numbers), sorted(stars)

            print("Invalid combination. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")

def simulate_draws(n, fixed_draw=None):
    """Simulate n draws and save the results in a DataFrame."""
    df = pd.DataFrame(columns=["Draw Number", "Chosen Number", "Winning Number"])
    count_matches = {i: 0 for i in range(8)}  # From 0 up to 7 matches

    for i in range(n):
        draw = generate_euromillions()
        ticket = generate_euromillions()
        matching_numbers, matching_stars = compare_results(draw, ticket)
        total_matches = matching_numbers + matching_stars
        count_matches[total_matches] += 1

        df.loc[i] = [
            i + 1,
            '-'.join(map(str, ticket[0])) + " | " + '-'.join(map(str, ticket[1])),
            '-'.join(map(str, draw[0])) + " | " + '-'.join(map(str, draw[1]))
        ]

    return count_matches, df

# Ask the user how many draws they want to simulate
num_draws = int(input("How many draws do you want to simulate? "))

# Ask the user if they want a fixed or random draw
draw_choice = input("Do you want to use a fixed combination for the draw? (yes/no) ").lower()
fixed_draw = None
if draw_choice == "yes":
    fixed_draw = get_fixed_combination()

# Simulation
count_matches, results_df = simulate_draws(num_draws)

# Print the summary of matches
print("\nSummary of matches:")
for matches, count in count_matches.items():
    percentage = (count / num_draws) * 100
    print(f"{matches} matches: {count} times ({percentage:.5f}%)")

# Ask if the user wants to save the results
save_choice = input("\nDo you want to save the results? (yes/no) ").lower()
if save_choice == "yes":
    filename = f"Simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    results_df.to_csv(filename, index=False)
    print(f"Results saved as {filename} in the current directory.")