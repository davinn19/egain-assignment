# Represents one portion of the chatbot's conversation (question and responses)
class DialogNode:
    def __init__(self, prompt: str):
        self.prompt = prompt

    def print_prompt(self):
        print(self.prompt)
    
    # Checks if a string is a recognizable input
    def is_valid_input(self, user_input: str):
        return True
    
    def execute(self):
        # Display the prompt and get the user's input for the first time
        self.print_prompt()
        user_input: str = input()

        # Repeat as long as the input is invalid
        while (self.is_valid_input(user_input) == False):
            print("Sorry, I didn't recognize your input. Please try again.")
            self.print_prompt()
            user_input: str = input()
        pass

        return user_input

    pass


# Dialog node for yes/no options
class ConfirmDialogNode(DialogNode):
    # Valid user responses
    yes_inputs: set[str] = {"y", "yes"}
    no_inputs: set[str] = {"n", "no"}

    def __init__(self, prompt: str):
        super.__init__(self, prompt)
    
    # Like regular print prompt but with a yes/no thing at the end
    def print_prompt(self):
        print(self.prompt)
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
        super.__init__(self, prompt)
        self.options = options

    # Displays available options in a numbered format after the prompt
    def print_prompt(self):
        super.print_prompt()
        for i in range(len(self.options)):
            print("({}) {}".format(i + 1, self.options[i]))
        pass

    # Checks if a string is one of the numbered options
    def is_valid_input(self, user_input: str):
        if user_input.isdigit() == False:
            return False
        
        number_input = int(user_input)
        return number_input >= 1 and number_input <= len(self.options)
    
    pass


if __name__ == "__main__":
    intro_node = ConfirmDialogNode(
        "Hi! I'm Davin, a chatbot designed to find your perfect laptop. Would you like my assistance"
    )

    budget_node = OptionsDialogNode(
        "What is your budget?",
        ["0-250", "250-500", "500-750", "750-1000", "1000+"],
    )

    use_case_node = OptionsDialogNode(
        "Which of the following best describes what you will use the laptop for?",
        ["Office Work", "Web Surfing", "Gaming", "Video Editing", "CAD"]
    )


    pass