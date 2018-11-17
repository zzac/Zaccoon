import json
import math

def title_bar(title): return "─" * math.ceil((72 - len(title)) / 2) + " " + title + " " + "─" * math.floor((72 - len(title)) / 2)

def menu(cr = True): print(("\n" if cr else "") + title_bar("ZACCOON") + "\nHere are the steps to create a custom password list :\n [1] Fill a form about your victim's informations (saved as a *.zin file).\n [2] Generate the password list (*.zin and *.zpa files required).\n\nHelp :\n [a] What is Zaccoon ?\n [b] What are *.zin files ?\n [c] What are *.zpa files ?\n\n[x] Exit\n")
menu(False)

exit = False
while not exit:
    a = input("[What do you want to do ?] > ").lower()
    if a in ["1", "2", "a", "b", "c", "x"]:
        if a == "1":
            qs = {
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
            infos = {}

            print("\n" + title_bar("YOUR VICTIM'S INFORMATIONS") + "\n* Provide as many answers and spellings as you can.\n* If you have multiple answers to a question, separate them with spaces.\n* Capital letters will be replaced by lowercase letters.\n* Just press [ENTER] if you do not have any answers to a question.\n")
            for q in qs: infos[q] = input("- " + qs[q] + " " + (33 - len(qs[q])) * "." + " ").lower().split(" ")
            json.dump(infos, open(input("\nFile name : ") + ".zin", "w"))
            print("\nThe information file has been created.")
            menu()

        elif a == "2":
            print("\n" + title_bar("PASSWORD LIST GENERATOR"))

            def question_bool(q):
                print(q)
                v = 0
                d = False
                while not d:
                    a = input("> ").lower()
                    if a in ["y", "n"]:
                        v = a == "y"
                        d = True
                    else: print("[Invalid answer]")
                return v
            def question_int(q):
                print(q)
                v = 0
                d = False
                while not d:
                    try:
                        v = int(input("> "))
                        d = True
                    except ValueError: print("[Invalid value]")
                return v
            def question_file(q, m = "r"):
                print(q)
                v = ""
                d = False
                while not d:
                    try:
                        v = open(input("> "), m)
                        d = True
                    except IOError: print("[Invalid file]")
                return v

            infos = json.load(question_file("- File that contains informations about your victim (*.zin)"))
            patterns = question_file("\n- File that contains the patterns to use (*.zpa)").read().split("\n")
            min = question_int("\n- Minimum password length (inclusive)")
            max = question_int("\n- Maximum password length (inclusive)")
            cap = question_bool("\n- Generate title case combinations ? [y/n]")
            output = question_file("\n- Output file name (choose the extension)", m = "w+")

            print("\nStart")
            err = False
            patterns = [x for x in patterns if "%" in x]
            pass_counter = 0
            for pattern in range(len(patterns)):
                try:
                    if "%" in patterns[pattern] and not patterns[pattern].startswith("#"):
                        print(" (%.2f" % ((pattern + 1) * 100 / len(patterns)) + "%) " + patterns[pattern])

                        pa = patterns[pattern].split("%", 1)[1].split("%")
                        l = len(pa)

                        po = 1
                        for p in pa: po *= len(infos[p]) if p in infos else 1

                        comb = [""] * po * (2 ** l if cap else 1)
                        for i in range(l):
                            a = 1
                            if i < l - 1:
                                for m in range(i + 1, l): a *= len(infos[pa[m]]) if pa[m] in infos else 1

                            for p in range(len(comb)):
                                w = pa[i][1:] if pa[i].startswith("$") else infos[pa[i]][math.floor(int(p / (2 ** l if cap else 1)) / a) % len(infos[pa[i]])]
                                comb[p] += w.title() if cap and math.floor(p % 2 ** l / 2 ** (l - i - 1)) % 2 == 1 else w

                        for c in comb:
                            if len(c) in range(min, max + 1) and c != "":
                                pass_counter += 1
                                output.write(c + "\n")

                except KeyError:
                    err = True
                    print("Invalid key : " + patterns[pattern])
                    break

            output.close()
            if not err: print("End (" + str(pass_counter) + " password" + ("s" if pass_counter > 1 else "") + " have been generated)")
            menu()

        elif a == "a": print("Zaccoon is a password list generator. It uses your victims' informations and patterns to create a list of weak passwords they might use.\n")
        elif a == "b": print("Zaccoon information files (*.zin) are files that contain your victims' informations. You can create one by entering [1].\n")
        elif a == "c": print("Zaccoon pattern files (*.zpa) are files that contain the patterns to use during password list generations.\n")
        else: exit = True

    else: print("[Invalid choice]")
