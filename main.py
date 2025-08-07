class DialogNode:
    
    def __init__(self, prompt: str, options: list,):
        self.prompt = prompt
        self.options = options

    pass

def print_options(options: list):
    for i in range(len(budget_options)):
        print("({}) {}".format(i + 1, options[i]))
    pass

if __name__ == "__main__":
    print("Intro")

    budget_options = ["0-250", "250-500", "500-750", "750-1000", "1000+"]
    print_options(budget_options)



    pass