#!/usr/bin/env python3
"""
Input: markdown guide with interleaved questions, questions.yml, output filepath
Output: content.json, readings files.
See content.schema.json for the format specification and sample_content.json for an example.
"""

import json
import sys, re 
from yaml import load, Loader
from os import path
import argparse
import markdown

def parse(guide_filename: str, questions_filename: str, out_filepath: str):
    """
    From an interleaved guide, write a content.json file.
    """
    with open(questions_filename, 'r') as fp:
        questions_yaml = load(fp, Loader)
    contents = {}
    sections = []
    secidx = 0
    qidx = 0
    ridx = 0
    order_l = []
    section = {}
    readings = {}
    questions = {}
    reading = []
    order_l = []
    section_title = ""
    section_count = 0
    total_questions = 0
    total_points = 0
    has_non_blank_line = False

    def add_section():
        nonlocal section, \
                sections, \
                order_l, \
                questions, \
                readings, \
                total_questions,\
                total_points,\
                has_non_blank_line 

        section["Count"] = section_count
        section["Title"] = section_title
        section["Order"] = order_l.copy()
        # section["Questions"] = questions.copy()
        # section["Readings"] = readings.copy()
        sections.append(section.copy())
        # total_questions += qidx#len(section["Questions"])
        # total_points += sum(
        #     map(
        #         lambda question: question["Points"],
        #         student_guide["Questions"].values()
        #     )
        # )
        # reset for next section
        section = {}
        order_l = []
        #questions = {}
        #readings = {}
        has_non_blank_line = False

    
    def add_reading():
        nonlocal reading, \
                readings, \
                ridx, \
                order_l, \
                has_non_blank_line
        if len(reading) > 0: 
            # render markdown to html and 
            # reading_title = f"Reading{ridx+1}"
            # reading_filename = f"{reading_title}.md"
            readings[str(ridx+1)] = markdown.markdown(''.join(reading), extensions=['markdown.extensions.fenced_code'])# replace with html reading_filename
            # order_l.append(reading_title)
            order_l.append(['r', str(ridx + 1)])
            # with open(path.join(out_filepath,"readings", f"{reading_title}.md"), 'w') as readingp:
            #     readingp.writelines(reading)
            reading=[]
            ridx += 1
            has_non_blank_line = False
    
    def add_question():
        nonlocal qidx, questions, order_l
        # question_title = f"Question{qidx+1}"
        questions[str(qidx+1)] = questions_yaml[qidx]
        # order_l.append(question_title)
        order_l.append(['q', str(qidx + 1)])
        qidx += 1


    # Parse sections
    with open(guide_filename, 'r') as fp:
        # Assume first line looks like this "# Guide Title"
        guide_title = fp.readline().split("# ")[1].strip()
        contents["ScenarioTitle"] = guide_title

        while line := fp.readline():

            # New section
            if next_match := re.match( 
                r"^## ",
                line
            ): 
                if secidx > 0:
                    add_reading()
                    add_section()

                reading.append(line)
                section_title = line[next_match.end():].strip()
                secidx += 1
                section_count = secidx 
                print(next_match)

            # Question markers look like this ^<question 1> or this ^<question>
            elif next_match := re.match( 
                r"^<question(\s+(?<= )\d*)?>",
                line
            ):
                print(next_match)
                add_reading()
                add_question()

            else:
                if not has_non_blank_line and not str.isspace(line):
                    has_non_blank_line = True
                if has_non_blank_line:
                    reading.append(line)

    # Finally, check if there are readings remaining and add final section
    add_reading()
    add_section()
    # Assemble final object and write.
    total_questions = len(questions)
    total_points = sum(
        map(
            lambda q: q["Points"],
            questions.values()
        )
    )
    student_guide = {
        "TotalQuestions" : total_questions,
        "TotalPoints" : total_points,
        "SectionOrder" : list(range(1, len(sections)+1)),
        "Sections" : sections.copy(),
        "Readings" : readings.copy(),
        "Questions": questions.copy(),
    }
    instructor_guide = {}
    contents["StudentGuide"] = student_guide
    contents["InstructorGuide"] = instructor_guide
    contents_json = json.dumps(contents, indent=4)
    with open(path.join(out_filepath, "content.json"), 'w') as contentp:
        contentp.writelines(contents_json)
        

def main():

    parser = argparse.ArgumentParser(description='Create a content.json file from a markdown guide and questions.yml')
    parser.add_argument('prod_path', metavar='PATH', type=str, nargs=1,help="path to the scenario prod folder")
    args = parser.parse_args()
    
    prod_path = args.prod_path[0]

    guide_filepath = path.join(prod_path, 'guide.md')
    questions_filepath = path.join(prod_path, 'questions.yml')
    out_filepath = path.join(prod_path, 'student_view')

    assert path.exists(guide_filepath)
    assert path.exists(questions_filepath)
    assert path.exists(out_filepath)

    parse(guide_filepath, questions_filepath, out_filepath)


if __name__ == "__main__":
    main()
