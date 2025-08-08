# Represents one portion of the chatbot's conversation (question and responses)
class DialogNode:
    def __init__(self, prompt: str):
        self.prompt = prompt

    # Displays the chatbot's spiel and any available options to the user
    def print_prompt(self):
        print(self.prompt)
    
    # Checks if a string is a recognizable input
    def is_valid_input(self, user_input: str):
        return True
    
    def execute(self):
        # Display the prompt and get the user's input for the first time
        print("")
        self.print_prompt()
        user_input: str = input()

        # Repeat as long as the input is invalid
        while (self.is_valid_input(user_input) == False):
            print("")
            print("Sorry, I couldn't understand your response. Please try again.")
            self.print_prompt()
            user_input: str = input()
        pass

        return user_input

    pass

# Dialog node that exits conversation after user input
class ExitNode(DialogNode):
    def __init__(self, prompt: str):
        self.prompt = prompt
    
    # Displays prompt and instructions to end convo
    def print_prompt(self):
        print(self.prompt)
        print("Press Enter to end the conversation.")
    
    def execute(self):
        super().execute()
        quit(0)

# Dialog node for yes/no options
class ConfirmDialogNode(DialogNode):
    # Valid user responses
    yes_inputs: set[str] = {"y", "yes"}
    no_inputs: set[str] = {"n", "no"}

    def __init__(self, prompt: str):
        super().__init__(prompt)
    
    # Like regular print prompt but with a yes/no thing at the end
    def print_prompt(self):
        super().print_prompt()
        print("[Y]es / [N]o")
    
    # Input must be some version of yes/no
    def is_valid_input(self, user_input: str):
        user_input = user_input.lower()
        return user_input in self.yes_inputs or user_input in self.no_inputs
    
    # Runs the dialog as normal but returns a 0 for no and 1 for yes
    def execute(self):
        result: str = super().execute()
        if result in self.yes_inputs:
            return 1
        return 0
    
    pass


# Dialog node for multiple options
class OptionsDialogNode(DialogNode):
    def __init__(self, prompt: str, options: list[str]):
        super().__init__(prompt)
        self.options = options

    # Displays available options in a numbered format after the prompt
    def print_prompt(self):
        super().print_prompt()
        for i in range(len(self.options)):
            print("({}) {}".format(i + 1, self.options[i]))
        pass

    # Checks if a string is one of the numbered options
    def is_valid_input(self, user_input: str):
        if user_input.isdigit() == False:
            return False
        
        number_input = int(user_input)
        return number_input >= 1 and number_input <= len(self.options)
    
    # Returns input in number form
    def execute(self):
        return int(super().execute())
    pass

class Laptop:
    def __init__(self, name: str, price: int, processing_tier: int, battery_life: int, storage: int, screen_tier: int):
        self.name = name
        self.price = price
        self.processing_tier = processing_tier
        self.battery_life = battery_life
        self.storage = storage
        self.screen_tier = screen_tier
        pass


if __name__ == "__main__":
    # Defining different laptop models
    laptops = [
        Laptop("CheapBook", 299, 1, 5, 256, 1),
        Laptop("Bell XYZ 13", 575, 2, 10, 750, 2),
        Laptop("HD Ghost 2 in 1", 999, 3, 8, 512, 3),
        Laptop("Mono Victis 15", 799, 4, 3, 2000, 4),
        Laptop("R7 Pro Super Max", 4500, 5, 18, 1000, 5)
    ]

    # Defining the different dialog nodes
    intro_node = ConfirmDialogNode(
        "Hi! I'm Davin, a chatbot designed to find your perfect laptop. Would you like my assistance?"
    )

    budget_node = OptionsDialogNode(
        "What is your budget?",
        ["$0-$250", "$250-$500", "$500-$750", "$750-$1000", "$1000+"],
    )

    use_case_node = OptionsDialogNode(
        "Which of the following best describes what you will use the laptop for?",
        ["Office Work", "Web Surfing", "Gaming", "Video Editing"]
    )

    early_exit_node = ExitNode(
        "No worries!"
    )

    recommend_node = ExitNode(
        "Sorry, I couldn't find a laptop within your budget."
    )

    # Start the conversation
    user_needs_help = intro_node.execute()

    if user_needs_help == False:
        early_exit_node.execute()
    
    budget = budget_node.execute()
    use_case = use_case_node.execute()

    # Find best laptop matching criteria
    best_laptop: Laptop = None
    best_laptop_score = 0

    max_price = 250 * budget
    if max_price > 1000:
        max_price = -1

    for laptop in laptops:
        # Price must be within budget
        if max_price != -1 and laptop.price > max_price:
            continue
        
        # Use laptop specs for score
        score = 0
        if use_case == 1:
            score = laptop.weight
        elif use_case == 2:
            score = laptop.price
        elif use_case == 3:
            score = laptop.processing_tier
        else:
            score = laptop.storage
        
        if score > best_laptop_score:
            best_laptop = laptop
            best_laptop_score = score

    # Display recommendation if necessary
    if best_laptop != None:
        recommend_node.prompt = "Based on your responses, I recommend the {}.".format(best_laptop.name)
    
    recommend_node.execute()
    pass