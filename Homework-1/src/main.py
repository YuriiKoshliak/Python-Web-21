from src.handlers import get_handler, load_notebook, show_birthdays


waiting = True
goodbyes = ("good bye", "close", "exit", "end", "bye")

# request-response cycle
def main_action(func):
    def inner(operator):
        try:
            func(operator)
        except AttributeError:
            print('Check twice or type the "help" to print the list of commands!')
        except Exception as e:
            message = str(e)
            print(message)
    
    return inner

@main_action
def main(operator) -> str:
    handler = get_handler(operator)

    print(handler(operator))

def entry_point():
    load = load_notebook(None)
    print(load) if load != None else None
    try:
        birthday_message = show_birthdays("7")
        if not birthday_message.startswith("Oh wow!"):
            print(f"Someone has a birthday soon: {birthday_message}")
    except TypeError as e:
        print("I need more information. Perhaps you should add a birthday to some contact.")
    while waiting == True:
        operator = input(":")
        if operator in goodbyes:
            main('goodbye')
            break 
        else: 
            main(operator)

if __name__ == '__main__':
    entry_point()
