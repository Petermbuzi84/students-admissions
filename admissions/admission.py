from admissions.generation import Generation
from admissions.printing import Printing


class Admission:
    def __init__(self):
        self.__no_option_selected = True
        self.__options = ["generate admission letters", "print admission letter"]
        self.__selected_option = ""

    def __validate_option(self, selection):
        if selection.isdigit():
            option_index = int(selection) - 1
            self.__selected_option = self.__options[option_index]
        elif selection == "q":
            self.__no_option_selected = False
        else:
            print("invalid selection, try again")

    def select_option(self):
        while self.__no_option_selected:
            for i in range(len(self.__options)):
                print(f"({i + 1}): {self.__options[i]}")
            print("(q): quit")
            selection = input("select option from the above list (e.g. 1) -> ")
            self.__validate_option(selection)
            if self.__no_option_selected:
                if self.__selected_option == self.__options[0]:
                    generate_letters = Generation()
                    generate_letters.admission_letters()
                elif self.__selected_option == self.__options[1]:
                    print_letters = Printing()
                    print_letters.admission_letters()
                else:
                    print("no selection, exiting program")
