import os
import datetime as dt


class UserInputs:
    def __init__(self, source_folder):
        self._no_source_file_selected = True
        self._no_school_selected = True
        self._no_reporting_date = True
        self.__source_file_list = os.listdir(source_folder)
        self._year = dt.datetime.now().strftime("%Y")
        self._reporting_date = self.__default_reporting_date(dt.datetime.now())
        self._selected_source_file = ""
        self._selected_schools = []
        self._min_marks = 0
        self._max_marks = 0
        self._max_pupils_per_school = 0

    def __default_reporting_date(self, date):
        return f"{date.strftime('%A')}, {self.__order(date.day)} {date.strftime('%B %Y')}"

    @staticmethod
    def __order(n):
        return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))

    def __validate_source_file_selection(self, in_selection):
        if in_selection.isdigit():
            source_file_index = int(in_selection) - 1
            if source_file_index < len(self.__source_file_list):
                self._selected_source_file = self.__source_file_list[source_file_index]
                # source file has been selected
                self._no_source_file_selected = False
            else:
                print("selected number is greater than available files, try again")
        elif in_selection == "q":
            # exit the source file selection function
            print("exit source file selection")
            self._no_source_file_selected = False
        else:
            # invalid selection request the user to enter the selection again
            print("invalid selection, should be numbers (e.g. 1)")

    def _source_file_selection(self):
        while self._no_source_file_selected:
            for i in range(len(self.__source_file_list)):
                print(f"({i + 1}): {self.__source_file_list[i]}")
            print("(q): quit")
            selection = input("select source file from the above list -> ")
            self.__validate_source_file_selection(selection)

    def __set_selected_schools(self, schools, selection_list):
        for selection in selection_list:
            school_index = int(selection) - 1
            self._selected_schools.append(schools[school_index])

    def __validate_school_selection(self, selection, schools):
        if selection.__contains__(","):
            split_selection = selection.split(",")
            split_selection = list(filter(lambda x: x.isdigit(), split_selection))
            self.__set_selected_schools(schools, split_selection)
            self._no_school_selected = False
        elif selection.isdigit():
            self.__set_selected_schools(schools, [selection])
            self._no_school_selected = False
        elif selection == "all":
            self.__set_selected_schools(schools, [i for i in range(1, len(schools)+1)])
            self._no_school_selected = False
        elif selection == "q":
            self._no_school_selected = False
        else:
            print("invalid selection, should be a list of number (e.g 1,2,3)")

    def _school_selection(self, schools):
        while self._no_school_selected:
            for i in range(len(schools)):
                print(f"({i + 1}): {schools[i]}")
            print("(all): for all schools")
            print("(q): quit")
            selection = input("select school from the above list -> ")
            self.__validate_school_selection(selection, schools)

    def _max_min_marks_range(self):
        while True:
            marks_range = input("enter the range of marks (e.g. 200-250) -> ")
            if marks_range.__contains__("-"):
                split_marks_range = marks_range.split("-")
                try:
                    self._min_marks = int(split_marks_range[0])
                    self._max_marks = int(split_marks_range[1])
                    break
                except Exception as e:
                    print(f"invalid range, {e}, try again")
            else:
                print("invalid range, try again")

    def _max_number_of_pupils_per_school(self):
        while True:
            number_per_school = input("enter the maximum number of pupils per school (e.g. 10) -> ")
            if number_per_school.isdigit():
                self._max_pupils_per_school = int(number_per_school)
                break
            else:
                print("invalid number, try again")

    def __retry_setting_reporting_date(self):
        retry = input("invalid date format, default date is set to today, do you want to try again (y/n) -> ")
        if retry == "y" or retry == "yes":
            self._no_reporting_date = True
        else:
            self._no_reporting_date = False

    def _set_reporting_date(self):
        while self._no_reporting_date:
            reporting_date = input("enter the reporting date ([day]/[month]/[year]) -> ")
            if reporting_date.__contains__("/"):
                try:
                    day, month, year = (int(x) for x in reporting_date.split('/'))
                    self._year = year
                    self._reporting_date = self.__default_reporting_date(dt.date(year, month, day))
                    self._no_reporting_date = False
                except Exception as e:
                    print(e)
                    self.__retry_setting_reporting_date()
            else:
                self.__retry_setting_reporting_date()
