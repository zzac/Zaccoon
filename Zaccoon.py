import json
import math

def title_bar(title): return "─" * math.ceil((72 - len(title)) / 2) + " " + title + " " + "─" * math.floor((72 - len(title)) / 2)
def menu(carriage_return = True): print(("\n" if carriage_return else "") + title_bar("ZACCOON") + "\nHere are the steps to create a custom password list :\n [1] Fill a form about your victim's informations (saved as a *.zin file).\n [2] Generate the password list (*.zin and *.zpa files required).\n\nHelp :\n [a] What is Zaccoon ?\n [b] What are *.zin files ?\n [c] What are *.zpa files ?\n\n[x] Exit\n")
menu(False)

exit = False
while not exit:
    choice = input("[What do you want to do ?] > ").lower()
    if choice in ["1", "2", "a", "b", "c", "x"]:
        if choice == "1":
            questions = {
                "name":       "Name(s)",
                "surname":    "Surname(s)",
                "nick":       "Nickname(s)",
                "first":      "First letter(s)",
                "age":        "Age(s)",
                "birthy":     "Birth year(s)",
                "birthm":     "Birth month(s)",
                "birthd":     "Birth day(s)",
                "country":    "Contry / countries",
                "city":       "City / cities",
                "family":     "Family member(s)",
                "birthp":     "Parent(s)'(s) birth year(s)",
                "friend":     "Friend(s)",
                "pet":        "Pet(s)",
                "company":    "Company / companies",
                "website":    "Website(s) used",
                "username":   "Username(s)",
                "star":       "Favorite celebrity / celebrities",
                "thing":      "Favorite thing(s)",
                "funny":      "Funny word(s)"
                }
            informations = {}

            print("\n" + title_bar("YOUR VICTIM'S INFORMATIONS") + "\n* Provide as many answers and spellings as you can.\n* If you have multiple answers to a question, separate them with spaces.\n* Capital letters will be replaced by lowercase letters.\n* Just press [ENTER] if you do not have any answers to a question.\n")
            for key in questions: informations[key] = input("- " + questions[key] + " " + (33 - len(questions[key])) * "." + " ").lower().split(" ")
            json.dump(informations, open(input("\nFile name : ") + ".zin", "w"))
            print("\nThe information file has been created.")
            menu()

        elif choice == "2":
            print("\n" + title_bar("PASSWORD LIST GENERATOR"))

            def question_bool(question):
                print(question)
                value = None
                done = False
                while not done:
                    answer = input("> ").lower()
                    if answer in ["y", "n"]:
                        value = answer == "y"
                        done = True
                    else: print("[Invalid answer]")
                return value
            def question_int(question):
                print(question)
                value = 0
                done = False
                while not done:
                    try:
                        value = int(input("> "))
                        done = True
                    except ValueError: print("[Invalid value]")
                return value
            def question_file(question, mode = "r"):
                print(question)
                value = ""
                done = False
                while not done:
                    try:
                        value = open(input("> "), mode)
                        done = True
                    except IOError: print("[Invalid file]")
                return value

            informations = json.load(question_file("- File that contains informations about your victim (*.zin)"))
            patterns = [line for line in question_file("\n- File that contains the patterns to use (*.zpa)").read().split("\n") if "%" in line]
            minimum = question_int("\n- Minimum password length (inclusive)")
            maximum = question_int("\n- Maximum password length (inclusive)")
            title_case = question_bool("\n- Generate title case combinations ? [y/n]")
            output = question_file("\n- Output file name (choose the extension)", "w")
            milliseconds = question_int("\n- Time to test one password on your dictionary attack software (in milliseconds)")

            print("\nStart")
            error = False
            password_counter = 0
            for i_pattern in range(len(patterns)):
                try:
                    if "%" in patterns[i_pattern] and not patterns[i_pattern].startswith("#"):
                        print(" (%.2f" % ((i_pattern + 1) * 100 / len(patterns)) + "%) " + patterns[i_pattern])

                        pattern_keys = patterns[i_pattern].split("%", 1)[1].split("%")

                        lower_possibilities = 1
                        for pattern_key in pattern_keys: lower_possibilities *= len(informations[pattern_key]) if pattern_key in informations else 1

                        combinations = [""] * lower_possibilities * (2 ** len(pattern_keys) if title_case else 1)
                        for i_pattern_key in range(len(pattern_keys)):
                            a = 1
                            if i_pattern_key < len(pattern_keys) - 1:
                                for k in range(i_pattern_key + 1, len(pattern_keys)): a *= len(informations[pattern_keys[k]]) if pattern_keys[k] in informations else 1

                            for i_combination in range(len(combinations)):
                                word = pattern_keys[i_pattern_key][1:] if pattern_keys[i_pattern_key].startswith("$") else informations[pattern_keys[i_pattern_key]][math.floor(int(i_combination / (2 ** len(pattern_keys) if title_case else 1)) / a) % len(informations[pattern_keys[i_pattern_key]])]
                                combinations[i_combination] += word.title() if title_case and math.floor(i_combination % 2 ** len(pattern_keys) / 2 ** (len(pattern_keys) - i_pattern_key - 1)) % 2 == 1 else word

                        for combination in combinations:
                            if len(combination) in range(minimum, maximum + 1) and combination != "":
                                password_counter += 1
                                output.write(combination + "\n")

                except KeyError:
                    error = True
                    print("Invalid key : " + patterns[i_pattern])
                    break

            output.close()

            seconds = milliseconds / 1000 * password_counter
            if not error: print("End (" + str(password_counter) + " password" + ("s" if password_counter > 1 else "") + " have been generated)\nExpected time to test all these passwords with your dictionary attack software : %dd %02dh %02dm %02ds" % (seconds / 86400, (seconds % 86400) / 3600, (seconds % 3600) / 60, seconds % 60))

            menu()

        elif choice == "a": print("Zaccoon is a password list generator. It uses your victims' informations and patterns to create a list of weak passwords they might use.\n")
        elif choice == "b": print("Zaccoon information files (*.zin) are files that contain your victims' informations. You can create one by entering [1].\n")
        elif choice == "c": print("Zaccoon pattern files (*.zpa) are files that contain the patterns to use during password list generations.\n")
        else: exit = True

    else: print("[Invalid choice]")
