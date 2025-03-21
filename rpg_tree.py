from tables.nodes.filenode import new_node


class StoryNode:
    """Represents a node in the decision tree."""
    def __init__(self, event_number, description, left = None, right = None):
        self.event_number = event_number
        self.description = description
        self.left_event = left
        self.right_event = right

class GameDecisionTree:
    """Binary decision tree for the RPG."""
    def __init__(self):     # empty decision tree
        self.nodes = {}
        self.root = None

    def insert(self, event_number, description, left_event, right_event):
        """Insert a new story node into the tree."""
        if event_number not in self.nodes:
            self.nodes[event_number] = StoryNode(event_number, description)

        node = self.nodes[event_number]
        node.description = description

        if self.root is None:
            self.root = node

        if left_event is not None:
            node.left_event = left_event
        if right_event is not None:
            node.right_event = right_event

    def play_game(self):
        """Interactive function that plays the RPG."""
        current = self.root
        choice = 0

        while choice != -1:
            print(f"{current.description}")          # showing description
            while True:
                try:
                    choice = int(input(" Which choice do you want to make? "         # asking for next choice
                                   + "Enter the number: "))
                    while choice != 1 and choice != 2:          # accounting for errors
                        print(" Sorry, that's not an option. Please pick from the selected options.")
                        choice = int(input(" Which choice do you want to make? "
                                + "Enter the number: "))
                    break                   # stops when either 1 or 2 is collected
                except ValueError:          # in case value is not a number
                    print(" Invalid input, please enter a number.")

            check = input(f" Is {choice} correct? Write \"yes\" or \"no\": ")       # checking if choice is correct
            check = check.lower()
            while check != "yes" and check != "no":                        # accounting for errors
                print(" Sorry, I don't understand. Please try again.")
                check = input(f" Is {choice} correct? Write \"yes\" or \"no\": ")
                check = check.lower()
            if check == "no":
                print(" Let's try again!")
                continue            # starts loop over again if choice was incorrect

            if choice == 1:       # traversing left or right
                current = self.nodes[current.left_event]
                if current.event_number < 0:
                    print(f"{current.description}")
                    break
            if choice == 2:
                current = self.nodes[current.right_event]
                if current.event_number < 0:
                    print(f"{current.description}")
                    break

        print(" Your story ends here. Thank you for playing.")

def load_story(filename, game_tree):
    """Load story from a file and construct the decision tree."""
    with open(filename, 'r') as story:
        for line in story:
            parts = line.strip().split('|')
            if len(parts) == 4:
                event_number = int(parts[0])
                description = parts[1]
                left_event = int(parts[2])
                right_event = int(parts[3])
                game_tree.insert(event_number, description, left_event, right_event)

# main program
if __name__ == "__main__":
    game_tree = GameDecisionTree()
    load_story("story.txt", game_tree)
    game_tree.play_game()