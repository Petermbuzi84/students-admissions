import os
from time import sleep
from utilities.support import log
from admissions_file.admission import Admission


class PrintAdmissionLetters(Admission):
    def __init__(self, source_file, sheet, year):
        super().__init__(source_file, sheet, year)
        self.print_max_multiplier = 0
        self.print_batch_size = 0
        self.batch_index = 1
        self.number_of_files_remaining = 0
        self.number_of_files = 0
        self.switched_folder_index = 0
        self.last_batch = False
        self.switch_state = False
        self.switched = False
        self.quit = False
        self.next_batch = False
        self.folder_index = 0

    def flip_document_selection(self, state):
        while True:
            command = self.flip_documents(state)
            if command == "r":
                self.switch_state = True
                break
            elif command == "q":
                self.quit = True
                break
            else:
                log("invalid selection, try again", status="warning")

    def flip_documents(self, state):
        if state == "odd":
            if self.next_batch:
                print("====================================")
                log("prepare documents to print the first batch of odd pages")
                print("====================================")
            else:
                print("====================================")
                log("flip the documents to print even pages")
                print("====================================")
                self.next_batch = True
            command = input("(r): ready (q): quit -> ")
            return command
        elif state == "even":
            if self.next_batch:
                print("====================================")
                log("prepare documents to print the next batch")
                print("====================================")
                self.number_of_files_remaining = self.number_of_files
            else:
                print("====================================")
                log("flip the documents to print even pages")
                print("====================================")
                self.next_batch = True
            command = input("(r): ready (q): quit -> ")
            return command
        return "q"

    def print_odd_even_admission_letters(self, state, admission_folder, admission_files):
        for admission in admission_files:
            if admission.__contains__(state):
                if self.print_max_multiplier < self.print_max_files \
                        and self.print_max_multiplier < self.number_of_files_remaining - 1:
                    if self.switched and self.folder_index == self.switched_folder_index and not self.last_batch:
                        pass
                    else:
                        log(f"multiplier {self.print_max_multiplier}")
                        self.printing(state, admission_folder, admission)
                    self.print_max_multiplier += 1
                else:
                    if self.print_max_multiplier == self.number_of_files_remaining - 1:
                        log("this is the last batch", status="warning")
                        self.last_batch = True
                        self.printing(state, admission_folder, admission)
                    self.print_batch_size = self.print_max_multiplier
                    log(f"multiplier {self.print_max_multiplier} else")
                    if self.switched:
                        self.printing(state, admission_folder, admission)
                    log(f"Printing {state} pages limit reached", status="warning")
                    log(f"{state} pages printed")
                    self.flip_document_selection(state)

    def printing(self, state, admission_folder, admission):
        path = f"{self.root_path}/{admission_folder}/{admission}"
        log(f"printing {self.batch_index} batches "
            f"of {self.print_max_files} {state} pages for {admission_folder}")
        # os.startfile(os.path.normpath(path), "print")
        sleep(5)

    def folder_loop(self, folder_list):
        if self.switched:
            return self.folder_index >= self.folder_index - self.print_batch_size
        return self.folder_index < len(folder_list)

    def read_and_print_admission_letters(self, state):
        if os.path.exists(self.root_path):
            print("====================================")
            log(f"printing {self.batch_index} batches of {self.print_max_files} {state} pages".upper())
            print("====================================")
            self.print_max_multiplier = 0
            folder_list = os.listdir(self.root_path)
            admission_folder = folder_list[self.folder_index]
            admission_files = os.listdir(f"{self.root_path}/{admission_folder}")
            while self.folder_loop(folder_list):
                log(f"printing folder at index {self.folder_index}")
                self.print_odd_even_admission_letters(state, admission_folder, admission_files)
                if self.switch_state:
                    self.switched = True
                    self.switched_folder_index = self.folder_index
                    self.number_of_files -= 1
                    break
                elif self.quit:
                    break
                else:
                    if self.switched:
                        self.folder_index -= 1
                    else:
                        self.number_of_files -= 1
                        self.folder_index += 1

    def print_admission_letters_with_one_sided_printer(self):
        if len(os.listdir("output/admission_letters")) > 0:
            self.number_of_files = len(os.listdir(self.root_path))
            self.number_of_files_remaining = len(os.listdir(self.root_path))
            while not self.last_batch:
                for state in self.states:
                    self.switch_state = False
                    self.read_and_print_admission_letters(state)
                    if self.quit:
                        self.number_of_files = 0
                        break
                self.batch_index += 1
                self.switched = False
                self.next_batch = False
                self.folder_index += self.print_max_files
                log(f"number of files remaining to be printed: {self.number_of_files_remaining} "
                    f"out of {len(os.listdir(self.root_path))}")
                if self.quit:
                    break
        else:
            log(f"no admission letters for pupils from {self.source_filename} found", status="warning")

    def admission_letters(self):
        self.get_print_max_files()
        print("===========================================================")
        log(f"beginning to print admission letters for pupils from {self.source_filename}...please wait")
        print("===========================================================")
        self.print_admission_letters_with_one_sided_printer()
        print("===========================================================")
        log(f"printing admission letters for pupils from {self.source_filename} complete", status="success")
        print("===========================================================")
