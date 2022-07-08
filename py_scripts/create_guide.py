#!/usr/bin/env python3
"""
Input: markdown guide with interleaved questions.
Output: content.json, readings files.
"""


import json
from flask import jsonify
import sys, re 
from yaml import load, Loader
from os import path

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
    questions = {}
    readings = {} 
    section = {}
    readings = {}
    questions = {}
    reading = []
    order_l = []
    section_title = ""
    section_count = 0

    def add_section():
        nonlocal section, sections, section_count, section_title, order_l, questions, readings
        section["count"] = section_count
        section["title"] = section_title
        section["order"] = ", ".join(order_l)
        section["questions"] = questions.copy()
        section["readings"] = readings.copy()
        sections.append(section.copy())
        # reset for next section
        section = {}
        order_l = []
        questions = {}
        readings = {}

    
    def add_reading():
        nonlocal reading, readings, ridx, order_l 
        if len(reading) > 0:
            reading_title = f"reading{ridx+1}"
            reading_filename = f"{reading_title}.md"
            readings[reading_title] = reading_filename
            order_l.append(reading_title)
            with open(path.join(out_filepath,"readings", f"{reading_title}.md"), 'w') as readingp:
                readingp.writelines(reading)
            #print(reading)
            reading=[]
            ridx += 1
    
    def add_question():
        nonlocal qidx, questions, questions_yaml, order_l
        question_title = f"question{qidx+1}"
        questions[question_title] = questions_yaml[qidx]
        order_l.append(question_title)
        qidx += 1


    # Parse sections
    with open(guide_filename, 'r') as fp:
        # Assume first line looks like this "# Guide Title"
        guide_title = fp.readline().split("# ")[1].strip()
        contents["title"] = guide_title

        while line := fp.readline():

            #print(line)
            if next_match := re.match( # section here: add reading, 
                r"^## \d\. ",
                line
            ): 
                if secidx > 0:
                    add_reading()
                    add_section()

                section_title = line[next_match.end():].strip()
                secidx += 1
                section_count = secidx 
                print(next_match)

            elif next_match := re.match( ## question here: add question to section, increment ridx
                r"^>>>>>>>",
                line
            ):
                print(next_match)
                add_reading()
                add_question()

            else:
                reading.append(line)

    # finally, check if there are readings remaining and add final section
    add_reading()
    add_section()
    contents["sections"] = sections.copy()
    contents_json = json.dumps(contents, indent=4)
    with open(path.join(out_filepath, "content.json"), 'w') as contentp:
        contentp.writelines(contents_json)
        

def main():
    """
    Usage: python3 create_guide.py GPATH QPATH OPATH 
    Where GPATH is the path to the guide file,
          QPATH is the path to the questions file,
          OPATH is the path to the output directory, [scenario]/student_view/
    """
    if len(sys.argv) < 4:
        exit()
    guide_filepath = sys.argv[1] 
    questions_filepath = sys.argv[2]
    out_filepath = sys.argv[3]
    parse(guide_filepath, questions_filepath, out_filepath)


if __name__ == "__main__":
    main()
