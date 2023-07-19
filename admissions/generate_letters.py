import os
from utilities.support import log
from docxtpl import DocxTemplate
from admissions_file.admission import Admission


class GenerateAdmissionLetters(Admission):
    def __init__(self, source_file, sheet, year):
        super().__init__(source_file, sheet, year)
        self.year = year
        self.total_pupils = 0
        self.school = ""

    def get_pupils_keys(self):
        index_key = ""
        school_name_key = ""
        for key in self.pupils.keys():
            if key.lower().__contains__("index"):
                index_key = key
            if key.lower().__contains__("school") and key.lower().__contains__("name"):
                school_name_key = key
        return index_key, school_name_key

    def clean_school_name(self, school_name, i):
        if i < self.pupils.shape[0]:
            school = self.pupils[school_name][i]
            school = school.replace(u"\xa0", u"")
            return school.strip(" ")
        return ""

    def generate_admission_letters_for_one_sided_printer(self):
        for state in self.states:
            doc = DocxTemplate(f"template/admission_one_side_printer/admission_{state}.docx")
            index_number, school_name = self.get_pupils_keys()
            i = 0
            multiplier = 0
            self.total_pupils = 0
            while i < self.pupils.shape[0]:
                if self.school != self.clean_school_name(school_name, i):
                    self.school = self.clean_school_name(school_name, i)
                    multiplier = 0
                if multiplier == self.pupils_per_school:
                    while self.clean_school_name(school_name, i) == self.school:
                        i += 1
                    self.school = self.clean_school_name(school_name, i)
                    multiplier = 0
                if i >= self.pupils.shape[0]:
                    break
                context = {
                    "student_name": self.pupils["NAME"][i],
                    "student_index": self.pupils[index_number][i],
                    "student_school": self.school,
                    "reporting_date": self.reporting,
                    "admission_year": self.year
                }
                student_details = f"admission letter for {context['student_name']} - {context['student_index']}"
                log(f"generating {student_details}")
                root_path = f"{self.root_path}/{context['student_index']}"
                if not os.path.exists(root_path):
                    os.makedirs(root_path)
                file_path = f"{root_path}/admission_{state}.docx"
                if os.path.exists(file_path):
                    log(f"{student_details} already exists", status="warning")
                else:
                    doc.render(context)
                    doc.save(file_path)
                    self.total_pupils += 1
                multiplier += 1
                i += 1

    def admission_letters(self):
        self.input_reporting_date()
        self.set_pupils_per_school()
        print(f"pupils will be reporting on {self.reporting}")
        print("===========================================================")
        log(f"beginning to generate admission letters for pupils from {self.source_filename}...please wait")
        print("===========================================================")
        self.generate_admission_letters_for_one_sided_printer()
        print("===========================================================")
        log(f"generation of admission letters for pupils from {self.source_filename} "
            f"complete...total pupils are {self.total_pupils}", status="success")
        log("admission letters are placed in the output/admission_letters folder")
        print("===========================================================")
