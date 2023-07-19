import os
import datetime as dt
from time import sleep
from admissions.printing_user_input import UserInput


class Printing(UserInput):
    def __init__(self):
        super().__init__()
        self.__output_folder = "output/admission_letters"
        self.__year = dt.datetime.now().strftime("%Y")
        self.__region_path = f"{self.__output_folder}/{self.__year}"
        self.__school_path = ""

    def __read_generated_admission_letters(self):
        if len(os.listdir(self.__output_folder)) > 0:
            self._regions = os.listdir(self.__region_path)
        else:
            print("no admission letters generated")

    def __set_school_list(self):
        for region in self._regions:
            if region == self._selected_region:
                self.__school_path = f"{self.__region_path}/{region}"
                schools = os.listdir(self.__school_path)
                self.__set_pupil_indices(schools, region)

    def __set_pupil_indices(self, schools, in_region):
        self._schools = {in_region: []}
        for school in schools:
            self._school_list.append(school)
            school_path = f"{self.__school_path}/{school}"
            pupils = os.listdir(school_path)
            self._schools[in_region].append({school: pupils})

    def __print_odd_and_even(self):
        states = ["odd", "even"]
        for state in states:
            print(f"printing admission {state} letters for pupils from {self._selected_school} "
                  f"in {self._selected_region} region")
            command = input("are you ready (y/n) -> ")
            if command == "y" or command == "yes":
                if state == "odd":
                    self.__print_odd_pages()
                elif state == "even":
                    self.__print_even_pages()

    def __print_odd_pages(self):
        selected_path = f"{self.__region_path}/{self._selected_region}/{self._selected_school}"
        for pupil in self._selected_pupils:
            admission_file_path = f"{selected_path}/{pupil}/admission_odd.docx"
            os.startfile(os.path.normpath(admission_file_path), "print")
            print(admission_file_path)
            sleep(5)

    def __print_even_pages(self):
        selected_path = f"{self.__region_path}/{self._selected_region}/{self._selected_school}"
        i = len(self._selected_pupils) - 1
        while i >= 0:
            pupil = self._selected_pupils[i]
            admission_file_path = f"{selected_path}/{pupil}/admission_even.docx"
            os.startfile(os.path.normpath(admission_file_path), "print")
            print(admission_file_path)
            sleep(5)
            i -= 1

    def admission_letters(self):
        self.__read_generated_admission_letters()
        self._select_region()
        if not self._selected_region:
            return
        self.__set_school_list()
        self._select_school()
        if not self._selected_school:
            return
        self._select_pupils()
        if not self._selected_pupils:
            return
        self.__print_odd_and_even()
