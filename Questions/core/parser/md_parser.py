from dataclasses import dataclass
from enum import Enum
import os
from typing import Optional
import re

import markdown
from bs4 import BeautifulSoup
import bs4

class Rating(Enum):
    Unknown = 0
    Easy = 1
    Medium = 2
    Hard = 3

class ExerciseType(Enum):
    Unknown = 0
    SHORT_ANSWER_WITH_SUB_QUESTIONS = 1
    SHORT_ANSWER = 2
    MULTIPLE_CHOICE = 3

@dataclass
class SimpleShortAnswerExercise:
    question : str
    answer : str

@dataclass
class ShortAnswerWithSubQuestion:
    main_content : str
    sub_questions : list[tuple[str, str]]       # tuple of [id, question_text]
    answers : list[tuple[str, str]]             # tuple of [id, question_text]. The id must match with id in sub_question

@dataclass
class MultipleChoiceExercise:
    question : str
    choices : list[tuple[str, str]]     # list of [id, question]. Id is used to match with answer
    answer : str                        # answer is a string, point to the id of choices

@dataclass
class Exercise:
    id : str = ""
    rate : Rating = Rating.Easy
    static_data : list[tuple[str, str]] = None   # tuple of file path, description
    type : ExerciseType = ExerciseType.Unknown
    data : MultipleChoiceExercise | SimpleShortAnswerExercise = None
    
    def validate(self):
        '''
            Validate data object type. Data object type must match with ExerciseType
        '''
        match (self.type):
            case (ExerciseType.SHORT_ANSWER):
                assert(isinstance(self.data, SimpleShortAnswerExercise))
            case (ExerciseType.MULTIPLE_CHOICE):
                assert(isinstance(self.data, MultipleChoiceExercise))
            case (ExerciseType.Unknown):
                raise Exception(f"Exercise type is unknown")
            case _:
                raise Exception(f"Invalid exercise type. Exercise type is object of {type(self.type)}")

@dataclass
class Module:
    name : str
    id : str
    exercises : list[Exercise]

class MDParser:
    _html : str = ""
    _soup : bs4.BeautifulSoup = None
    def __init__(self, md_file : str):
        # Check path exists and markdown file valid
        if not os.path.exists(md_file) and not md_file.endswith(md_file):
            raise Exception(f"File {md_file} is not valid markdown file")
        
        # Get html repr of .md file and push it to bs4 for parsing
        with open(md_file, "r") as f:
            self._html = markdown.markdown(f.read())
        self._soup = BeautifulSoup(self._html, "html.parser")
    
    def get_raw_chapter_name(self):
        return self._soup.find("h1").text
    
    def _get_module_id_and_name(self, text) -> tuple[str, str]:
        # Match pattern for module tile in format <chapter_num>.<module_num>. <module_name>
        pattern = re.compile(r"(^\d{1,2}\.\d{1,2})[\.\s]{1,3}([\w,\s]+)")
        match_re = pattern.fullmatch(text)
        if not match_re:
            raise Exception("Title of the module is out of format. It should be <chapter_num>.<module_num>. <module_name>. For example: 2.1. Độ dịch chuyển")

        id = match_re.group(1)
        name = match_re.group(2)

        return (id.strip(), name.strip())
    
    def _get_question_id_and_rating(self, text) -> tuple[str, Rating]:
        # For better and more flexibility syntax, normalize the pattern to lower-case
        norm_text = text.lower()

        # Rating and ID are separated by (-)
        parts = [p.strip() for p in norm_text.split("-")]
        assert(len(parts) == 2)

        # Match rating with Rating.name
        rating_regex_pattern = re.compile(f"({Rating.Easy.name.lower()}|{Rating.Medium.name.lower()}|{Rating.Hard.name.lower()})")
        match_rating = rating_regex_pattern.match(parts[1])
        if not match_rating:
            raise Exception(f"Invalid rating in {text}. Rating must be {Rating.Easy.name} or {Rating.Medium.name} or {Rating.Hard.name}")
        rating : Rating = Rating.Unknown
        match (match_rating.group(1)):
            case "easy":
                rating = Rating.Easy
            case "medium":
                rating = Rating.Medium
            case "hard":
                rating = Rating.Hard
            case _:
                raise Exception(f"Check matching group {str(match_rating.group(1))}")

        # id must be <chapter>.<module>.<num>, such as 2.1.2
        id_regex_pattern = re.compile(r".*(\d{1,2}\.\d{1,2}\.\d{1,2})")
        match_id = id_regex_pattern.match(parts[0])
        if not match_id:
            raise Exception(f"Invalid exercise ID. Cannot find ID in {text}")
        id = match_id.group(1)
        return (id, rating)

    def get_exercise_type(self, question_elements : list[bs4.PageElement]):
        # Multiple choice should startswith this
        choices = ["(A)", "(B)", "(C)", "(D)"]
        choices_match = {}

        for el in question_elements:
            if el.name == "p":
                # Check match with multiple choice. If match, set the choices_match to True
                for choice in choices:
                    if el.text.strip().startswith(choice):
                        choices_match[choice] = True
        
        # if there is at least 1 match -> Multiple choice
        if len(choices_match.keys()) > 0:
            # if not enough 4 choice
            if len(choices_match.keys()) != len(choices):
                raise ValueError("Question is type MultipleChoice, but do not have 4 choices. Please check question:\n{}".format("\n".join(element.text for element in question_elements)))
            else:
                return ExerciseType.MULTIPLE_CHOICE

        # if no match, should be short answer
        return ExerciseType.SHORT_ANSWER

    def _fill_multiple_choice(self, exercise : Exercise, question_texts : list[str], answer_texts):
        # get regex for choice. Choice starts with (A), (B), (C), (D)
        re_choice_pattern = re.compile(r"^\([A-D]\)")
        choices = []
        question_lines = []
        for line in question_texts:
            choice_match = re_choice_pattern.search(line.strip())
            if choice_match:
                # Use choice letter as ID
                choice_id = choice_match.group(0)
                choice_data = line.strip().removeprefix(choice_id).strip()

                if (any(choice_id == id for id, _ in choices)):
                    raise Exception(f"Choice {line} is duplicated")
                choices.append((choice_id, choice_data))
            else:
                question_lines.append(line)
        
        assert(len(choices) == 4)   # Must be 4

        for line in answer_texts:
            # Find regex match with choice letter. This must be the same with choice
            answer_match = re_choice_pattern.search(line)
            if answer_match:
                answer = answer_match.group(0)
                break
        else:
            raise Exception(f"Cannot find answer from text {"\n".join(answer_texts)}")
        
        # answer must match with one of choice
        assert(any(id == answer for id, _ in choices))
        exercise.data = MultipleChoiceExercise("\n".join(question_lines), choices, answer)
    
    def _fill_short_answers_with_sub_questions(self, exercise : Exercise, question_texts : list[str], answer_texts):
        
        # get regex for subquestion. subquestion starts with (a), (b), ...
        re_sub_question_pattern = re.compile(r"^\([a-z]\)")
        sub_questions = []
        question_lines = []
        answers = []
        for line in question_texts:
            sub_question_match = re_sub_question_pattern.search(line.strip())
            if sub_question_match:
                # use letter (a), (b), ... for question id
                sub_question_id = sub_question_match.group(0)
                sub_question_data = line.strip().removeprefix(sub_question_id).strip()
                
                # check for any duplicate
                if any(sub_question_id == id for id, _ in sub_questions):
                    raise Exception(f"Sub-question {line} is duplicated")
                sub_questions.append((sub_question_id, sub_question_data))
            else:
                question_lines.append(line)
        
        for line in answer_texts:
            answer_match = re_sub_question_pattern.search(line)
            if answer_match:
                # use letter (a), (b), ... for answer id. This must be the same as question_id
                answer_id = answer_match.group(0)
                answer_data = line.strip().removeprefix(answer_id).strip()
                answers.append((answer_id, answer_data))
                assert(any(id == answer_id for id, _ in sub_questions))
        
        # answers and sub_questions must be same size
        assert(len(answers) == len(sub_questions))
        exercise.data = ShortAnswerWithSubQuestion("\n".join(question_lines), sub_questions, answers)
    
    def _fill_simple_short_answers(self, exercise : Exercise, question_texts : list[str], answer_texts):
        exercise.data = SimpleShortAnswerExercise(
            question="\n".join(question_texts),
            answer="\n".join(answer_texts)
        )

    def _fill_question_and_answer_from_element_list(self, exercise: Exercise, question_elements : list[bs4.PageElement], answer_elements : list[bs4.PageElement]):
        exercise.type = self.get_exercise_type(question_elements)
        question_texts = [element.text for element in question_elements if element.name == "p"]
        answer_texts = [element.text for element in answer_elements if element.name == "p"]
        match (exercise.type):
            case (ExerciseType.MULTIPLE_CHOICE):
                self._fill_multiple_choice(exercise, question_texts, answer_texts)
            case (ExerciseType.SHORT_ANSWER_WITH_SUB_QUESTIONS):
                self._fill_short_answers_with_sub_questions(exercise, question_texts, answer_texts)
            case (ExerciseType.SHORT_ANSWER):
                self._fill_simple_short_answers(exercise, question_texts, answer_texts)

    def _fill_static_data(self, exercise : Exercise, question_elements : list[bs4.PageElement]):
        exercise.static_data = []
        for el in question_elements:
            # for now, only image is the static data
            if el.find("img"):
                img_el = el.find("img")
                try:
                    desc = img_el["alt"]
                except KeyError:
                    desc = ""
                link = img_el["src"]
                exercise.static_data.append((link, desc))

    def get_module_exercises(self, elements : list[bs4.PageElement]) -> list[Exercise]:
        element : bs4.PageElement
        exercises = []
        current_exercise : Exercise = None
        question_elements : list[bs4.PageElement] = []
        answer_elements : list[bs4.PageElement] = []
        insert_question = True
        for element in elements:
            if element.name == "h3":                
                if current_exercise:
                    self._fill_question_and_answer_from_element_list(current_exercise, question_elements, answer_elements)
                    self._fill_static_data(current_exercise, question_elements)
                    question_elements = []
                    answer_elements = []
                    current_exercise.validate()
                    exercises.append(current_exercise)

                id, rating = self._get_question_id_and_rating(element.text)
                insert_question = True
                current_exercise = Exercise()
                current_exercise.id = id
                current_exercise.rating = rating
                current_exercise.static_data = []

            elif element.name == "h4":
                insert_question = False
            elif element.name in ["p", "blockquote"]:
                # Check element in ["p", "blockquote"] only. Ignore empty element such as '\n'
                if insert_question:
                    question_elements.append(element)
                else:
                    answer_elements.append(element)

        # Check and add last exercise
        if current_exercise:
            self._fill_question_and_answer_from_element_list(current_exercise, question_elements, answer_elements)
            self._fill_static_data(current_exercise, question_elements)
            current_exercise.validate()
            exercises.append(current_exercise)
        return exercises
    
    def get_modules(self) -> list[Module]:
        modules = []

        child : bs4.PageElement
        current_module : Module = None
        exercise_elements : list[bs4.PageElment] = []
    
        for child in self._soup.children:
            if child.name == "h1":
                pass
            elif child.name == "h2":
                # Level 2 heading is used solely for module name 
                if exercise_elements:
                    current_module.exercises = self.get_module_exercises(exercise_elements)
                    exercise_elements = []
                    modules.append(current_module)
                    current_module = None

                id, name = self._get_module_id_and_name(child.text)
                current_module = Module(name=name, id=id, exercises=[])
            elif child.name in ["h3", "h4", "p", "blockquote"]:
                # Check element in ["h3", "h4", "p", "blockquote"] only. Ignore empty element such as '\n'
                exercise_elements.append(child)
        
        # add last module
        if current_module:
            if exercise_elements:
                current_module.exercises = self.get_module_exercises(exercise_elements)
                exercise_elements = []
            modules.append(current_module)
        return modules


if __name__ == "__main__":
    md_file = "../../chapter-02/questions.md"
    parser = MDParser(md_file)
    modules = parser.get_modules()
    print(modules[0].exercises)