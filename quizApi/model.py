from sqlmodel import Field, SQLModel, create_engine,Session,select,Relationship
from enum import Enum
from datetime import datetime
from typing import Annotated,Optional

class Course(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    program_id : int
    instructor_id : int
    course_name: str
    topics : list["Topic"] = Relationship(back_populates="course")  # one to many
    quizes : list["Quiz"] = Relationship(back_populates="course")  # one to many or #one to one


class Topic(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    course_id: int | None = Field(default=None, foreign_key="course.id")
    topic_name: str
    topic_description: str
    course: Course = Relationship(back_populates="topics") # many to one
    contents: list["Content"] = Relationship(back_populates="topic") # one to many
    quiz_topics: list["QuizTopics"] = Relationship(back_populates="topic") # one to many

class Content(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    topic_id : Optional[int] = Field(foreign_key="topic.id")
    topic: Topic = Relationship(back_populates="contents") # many to one

class Quiz(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    course_id: int | None = Field(default=None, foreign_key="course.id")
    quiz_name: str
    quiz_time: datetime
    quiz_description : str
    course: Course = Relationship(back_populates="quizes") # many to one
    answer_sheets: list["AnswerSheet"] = Relationship(back_populates="quiz") # one to many
    quiz_topics: list["QuizTopics"] = Relationship(back_populates="quiz") # one to many


class QuizTopics(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    topic_id: int | None = Field(default=None, foreign_key="topic.id")
    parent_quiz_topic_id: int | None = Field(default=None, foreign_key="quiztopics.id")
    quiz_name : str|None = None
    quiz: Quiz = Relationship(back_populates="quiz_topics") # many to one
    topic: Topic = Relationship(back_populates="quiz_topics") # many to one

class QuestionType(str, Enum):
    single_select = "single_select"
    multi_select = "multi_select"
    case_study = "case_study"
    free_text = "free_text"
    code_questions = "code_questions"
    



class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    question_text: str
    question_type: QuestionType
    question_points: int
    single_select_mcqs: "SingleSelectMcqs" = Relationship(back_populates="question")
    multi_select_mcqs: "MultiSelectMcqs" = Relationship(back_populates="question")
    coding_questions: "CodingQuestions" = Relationship(back_populates="question")
    
    
class McqsType(str,Enum):
    type1: str = "Type 1"
    type2: str = "Type 2"
    type3: str = "Type 3"
    type4: str = "Type 4"    


  
class SingleSelectMcqs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    mcqs_type: McqsType
    question: Question = Relationship(back_populates="single_select_mcqs") # one to one
    options: list["SingleOptions"] = Relationship(back_populates="single_select_mcqs") # one to many
    case_studies: list["CaseStudy"] = Relationship(back_populates="single_select_mcqs")




class SingleOptions(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    single_select_id : int | None = Field(default=None, foreign_key="singleselectmcqs.id")
    option_text : str
    is_correct : bool
    single_select_mcqs: SingleSelectMcqs = Relationship(back_populates="options") # many to one
    

class MultiSelectMcqs(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    mcqs_id: int
    question: Question = Relationship(back_populates="multi_select_mcqs") # one to one
    options: list["OptionMultiSelectQuestions"] = Relationship(back_populates="multi_select_mcqs") # one to many


    
class OptionMultiSelectQuestions(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    multi_select_id : int | None = Field(default=None, foreign_key="multiselectmcqs.id")
    option_text : str
    is_correct : bool
    multi_select_mcqs: MultiSelectMcqs = Relationship(back_populates="options") # many to one



class CaseStudy(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    single_select_mcqs_id: int | None = Field(default=None, foreign_key="singleselectmcqs.id")
    mcqs_id : int
    single_select_mcqs: SingleSelectMcqs = Relationship(back_populates="case_studies")  

class CodingQuestions(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    is_correct: bool
    question: Question = Relationship(back_populates="coding_questions") # one to one




class AnswerSheet(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    quiz_status: str
    start_date: datetime  
    end_date: datetime   
    answers: list["Answer"] = Relationship(back_populates="answer_sheet") # one to many
    quiz: Quiz = Relationship(back_populates="answer_sheets")  # Define the relationship with Quiz

class Answer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    correct_answer: str
    points_received: int
    answer_sheet_id: Optional[int] = Field(default=None, foreign_key="answersheet.id")
    answer_sheet: AnswerSheet = Relationship(back_populates="answers")  # many to one
    single_select_mcqs_ans: list["SingleSelectMcqsAns"] = Relationship(back_populates="answer")  # one to many
    multi_select_mcqs_ans: list["MultiSelectMcqsAns"] = Relationship(back_populates="answer")  # one to many
    case_study_ans: list["CaseStudyAns"] = Relationship(back_populates="answer")  # one to many
    coding_questions_answer: list["CodingQuestionsAnswer"] = Relationship(back_populates="answer")  # one to many


class SingleSelectMcqsAns(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    answer_id: int | None = Field(default=None, foreign_key="answer.id")
    mcqs_id: int
    selected_mcqs_id: int
    answer: Answer = Relationship(back_populates="single_select_mcqs_ans") # many to one


    


class MultiSelectMcqsAns(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    answer_id: int | None = Field(default=None, foreign_key="answer.id")
    mcqs_id: int
    answer: Answer = Relationship(back_populates="multi_select_mcqs_ans") # many to one
    options: list["OptionMultiSelectAnswer"] = Relationship(back_populates="multi_select_mcqs_ans") # one to many

class OptionMultiSelectAnswer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    multiselect_mcqs_ans_id: int | None = Field(default=None, foreign_key="multiselectmcqsans.id")
    selected_mcqs_id: int
    multi_select_mcqs_ans: MultiSelectMcqsAns = Relationship(back_populates="options") # many to one

class CaseStudyAns(SQLModel,table=True):
    id : int | None = Field(default=None, primary_key=True)
    answer_id : int | None = Field(default=None, foreign_key="answer.id")
    answer: Answer = Relationship(back_populates="case_study_ans") # many to one
    join_case_study_answer: list["JoinCaseStudyAnswer"] = Relationship(back_populates="case_study_ans") # one to many


class JoinCaseStudyAnswer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    case_study_ans_id: int | None = Field(default=None, foreign_key="casestudyans.id")
    single_select_mcq_answer_id: int
    case_study_ans: CaseStudyAns = Relationship(back_populates="join_case_study_answer")


class CodingQuestionsAnswer(SQLModel,table=True):
    id : int | None = Field(default=None, primary_key=True)
    answer_id : int | None = Field(default=None, foreign_key="answer.id")
    field_answer : str
    answer: Answer = Relationship(back_populates="coding_questions_answer") # many to one
