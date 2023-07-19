
class UserInput:
    def __init__(self):
        self._regions = []
        self._school_list = []
        self._selected_region = ""
        self._selected_school = ""
        self._selected_pupils = []
        self._schools = {}
        self.__no_region_selected = True
        self.__no_school_selected = True
        self.__no_pupil_selected = True

    def __validate_region(self, selection):
        if selection.isdigit():
            region_index = int(selection) - 1
            if region_index < len(self._regions):
                self._selected_region = self._regions[region_index]
                self.__no_region_selected = False
            else:
                print("selected region is out of range from the list, try again")
        elif selection == "q":
            self.__no_region_selected = False
        else:
            print("invalid selection, should be numbers, try again")

    def _select_region(self):
        while self.__no_region_selected:
            for i in range(len(self._regions)):
                print(f"({i + 1}): {self._regions[i]}")
            print("(q): quit")
            selection = input("select region from the above list (e.g. 1) -> ")
            self.__validate_region(selection)

    def __validate_school(self, selection):
        if selection.isdigit():
            school_index = int(selection) - 1
            if school_index < len(self._school_list):
                self._selected_school = self._school_list[school_index]
                self.__no_school_selected = False
            else:
                print("selected school is out of range from the list, try again")
        elif selection == "q":
            self.__no_school_selected = False
        else:
            print("invalid selection, should be numbers, try again")

    def _select_school(self):
        while self.__no_school_selected:
            for i in range(len(self._school_list)):
                print(f"({i + 1}): {self._school_list[i]}")
            print("(q): quit")
            selection = input(f"select school for {self._selected_region} region from the above list (e.g. 1) -> ")
            self.__validate_school(selection)

    def __set_selected_pupils(self, pupils, selection):
        pupil_index = int(selection) - 1
        if pupil_index < len(pupils):
            self._selected_pupils.append(pupils[pupil_index])
            self.__no_pupil_selected = False
        else:
            print("selected pupils is out of range from the list, try again")

    def __validate_pupils(self, pupils, selection):
        if selection.__contains__(","):
            split_selection = selection.split(",")
            split_selection = list(filter(lambda x: (x.isdigit() and int(x) - 1 < len(pupils)), split_selection))
            for select in split_selection:
                self.__set_selected_pupils(pupils, select)
        elif selection == "all":
            self._selected_pupils = pupils
            self.__no_pupil_selected = False
        elif selection.isdigit():
            self.__set_selected_pupils(pupils, selection)
        elif selection == "q":
            self.__no_pupil_selected = False
        else:
            print("invalid selection, should be numbers, try again")

    def _select_pupils(self):
        while self.__no_pupil_selected:
            region = self._schools
            if self._selected_region in region:
                schools = region[self._selected_region]
                for school in schools:
                    if self._selected_school in school.keys():
                        pupils = school[self._selected_school]
                        for i in range(len(pupils)):
                            print(f"({i + 1}): {pupils[i]}")
                        print("(all): for all pupils")
                        print("(q): quit")
                        selection = input(f"select pupils from {self._selected_school} "
                                          f"in {self._selected_region} from the above list (e.g. 1,2,3) -> ")
                        self.__validate_pupils(pupils, selection)
                        if not self.__no_pupil_selected:
                            break
                    else:
                        self.__no_pupil_selected = False
            else:
                self.__no_pupil_selected = False
