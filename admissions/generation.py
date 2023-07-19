import os
import pandas as pd
from docxtpl import DocxTemplate
from admissions.generation_user_input import UserInputs


g_pupils = pd.DataFrame({})


class Generation(UserInputs):
    def __init__(self):
        self.__source_folder = "source/admissions"
        super().__init__(self.__source_folder)
        self.__output_folder = "output/admission_letters"
        self.__template_even_page_document = "template/admission_one_side_printer/admission_even.docx"
        self.__school_list = []
        self.__pupils_by_school = {}
        self.pupils = pd.DataFrame({})
        self.__pupil_count = 0
        self.__current_region = ""
        self.__pupil_count_limit_reached = False

    def __source_file_headings(self):
        headings = self.pupils.keys()
        index_no = ""
        pupil_name = ""
        pupil_marks = ""
        pupil_gender = ""
        school_name = ""
        for heading in headings:
            if heading.lower().__contains__("index"):
                index_no = heading
            elif heading.lower().__contains__("school") and heading.lower().__contains__("name"):
                school_name = heading
            elif heading.lower() == "name":
                pupil_name = heading
            elif heading.lower().__contains__("tot"):
                pupil_marks = heading
            elif heading.lower().__contains__("ge"):
                pupil_gender = heading
        return [index_no, pupil_name, pupil_gender, pupil_marks, school_name]

    def __group_pupils_by_school(self, school_name):
        headings = self.__source_file_headings()
        self.__pupils_by_school[school_name] = []
        for i in range(self.pupils.shape[0]):
            local_school_name = self.__get_school_name(i)
            if local_school_name == school_name:
                pupil = self.__get_pupil_details(i)
                self.__pupils_by_school[school_name].append({
                    "index": pupil[headings[0]],
                    "name": pupil[headings[1]],
                    "gender": pupil[headings[2]],
                    "marks": pupil[headings[3]]
                })

    def __output_admission_letters(self):
        source_name = self.__get_source_file_name()
        for school in self.__school_list:
            pupil_list_per_school = self.__pupils_by_school[school]
            for pupil in pupil_list_per_school:
                pupil_index = pupil["index"]
                if self.__pupil_count_limit_reached:
                    self.__pupil_count_limit_reached = False
                    self.__pupil_count = 0
                    break
                elif school in self._selected_schools:
                    output_path = f"{self.__output_folder}/{self._year}/{source_name}/{school}/{pupil_index}"
                    self.__filter_pupil_gender(pupil, school, output_path)

    def __filter_pupil_gender(self, pupil, school, output_path):
        pupil_gender = pupil["gender"]
        if pupil_gender == "F":
            self.__filter_pupil_marks(pupil, school, output_path)

    def __filter_pupil_marks(self, pupil, school, output_path):
        pupil_marks = str(pupil["marks"]).strip()
        if pupil_marks != '' and self._min_marks <= int(pupil_marks) <= self._max_marks:
            self.__filter_pupils_by_number_per_school(pupil, school, output_path)

    def __filter_pupils_by_number_per_school(self, pupil, school, output_path):
        if self.__pupil_count == self._max_pupils_per_school:
            self.__pupil_count_limit_reached = True
        else:
            self.__pupil_count += 1
            self.__create_folder(output_path)
            self.__generate_admission_letters(pupil, school, output_path)

    def __generate_admission_letters(self, pupil, school, output_path):
        states = ["odd", "even"]
        context = {
            "student_name": pupil["name"],
            "student_index": pupil["index"],
            "student_school": school,
            "reporting_date": self._reporting_date,
            "admission_year": self._year
        }
        for state in states:
            output_file_path = f"{output_path}/admission_{state}.docx"
            if os.path.exists(output_file_path):
                print(f"{output_file_path} already exists")
            else:
                print(f"generating {output_file_path}")
                template_path = f"template/admission_one_side_printer/admission_{state}.docx"
                doc = DocxTemplate(template_path)
                doc.render(context)
                doc.save(output_file_path)

    def __set_listed_schools(self):
        current_school = ""
        for i in range(self.pupils.shape[0]):
            school_name = self.__get_school_name(i)
            if school_name != current_school:
                current_school = school_name
                self.__school_list.append(school_name)
                self.__group_pupils_by_school(school_name)

    @staticmethod
    def __get_source_file_sheet_name(source_file_path):
        preload_excel = pd.ExcelFile(source_file_path)
        return preload_excel.sheet_names[0]

    @staticmethod
    def __clean_school_name(school_name):
        name = school_name.replace(u"\xa0", u"")
        name = name.strip(" ")
        return name

    @staticmethod
    def __create_folder(path):
        if not os.path.exists(path):
            if path.__contains__("/"):
                os.makedirs(path)
            else:
                os.mkdir(path)

    def __get_pupil_details(self, index):
        headings = self.__source_file_headings()
        return self.pupils[headings].iloc[index]

    def __get_school_name(self, index):
        headings = self.__source_file_headings()
        pupil_details = self.__get_pupil_details(index)
        return self.__clean_school_name(pupil_details[headings[4]])

    def __get_source_file_name(self):
        split_source_file = self._selected_source_file.split(".xlsx")
        return split_source_file[0]

    def __load_source_file(self):
        global g_pupils
        source_file_path = f"{self.__source_folder}/{self._selected_source_file}"
        source_file_name = self.__get_source_file_name()
        if g_pupils.shape[0] == 0 or self.__current_region.lower() != source_file_name.lower():
            print(f"loading {self._selected_source_file}")
            sheet = self.__get_source_file_sheet_name(source_file_path)
            g_pupils = pd.read_excel(source_file_path, sheet_name=sheet)
            self.__current_region = source_file_name
        else:
            print(f"{self._selected_source_file} already loaded in memory")
        self.pupils = g_pupils

    def admission_letters(self):
        self._source_file_selection()
        if self._selected_source_file != "":
            self.__load_source_file()
            self.__set_listed_schools()
            self._max_min_marks_range()
            self._max_number_of_pupils_per_school()
            self._set_reporting_date()
            self._school_selection(self.__school_list)
            self.__output_admission_letters()
