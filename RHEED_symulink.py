import os 
import re
from collections import namedtuple

def extract_three_digit_numbers(path):
    return re.findall(r'(?<!\d)\d{3}(?!\d)', path)

def extract_three_digits_after_240(path):
    return re.findall(r'240(\d{3})', path)

def extract_three_digits_after_230(path):
    return re.findall(r'230(\d{3})', path)

def extract_three_digits_after_20190(path):
    return re.findall(r'20190(\d{3})', path)

def file_to_project(filepath, timestamps):
    # filepath is a python Path object that specifies the file to categorize.
    # It is relative to the root directory of the data source. So, for example,
    # for the file /srv/zpool01/paradim-data/paradim-rheed1-images/moly_64_endGrowthCool.imm
    # filepath = Path("./moly_64_endGrowthCool.imm")
    # while for the file /srv/zpool01/paradim-data/paradim-rheed1-images/329/SAO_11_end_cold_0.img
    # filepath = Path("./329/SAO_11_end_cold_0.img")
    # timestamps is a NamedTuple with the elements: created_at, modified_at
    #    Where timestamps.created_at is the time (in unix seconds) at which the file was created,
    #    and timestamps.modified_at is the time (in unix seconds) at which the file was last modified.
    #
    # From this information, the function needs to decide where the file belongs. The return
    # value must be a NamedTuple or Object with the following elements:
    #    project_id : integer (or None), the project number the file is associated with.
    #                 e.g. 329 or 126 or None if unknown.
    #    folder_path : the path, excluding filename (or None), where this object should appear in the project data. 
    #                  e.g. "rheed1/02-28-2024" or "mbe/05-16-2025/Sample116" or None if unknown.
    #    confidence : integer representing the confidence in the assignment
    #                 e.g. 3=HIGH, 2=MEDIUM, 1=LOW, 0=NONE.
    #                 If HIGH, the other two parameters MUST NOT be None.
    # The returned object/tuple can contain other elements as well, but must contain these three.

    if not filepath:
        raise ValueError("ERROR: a file path is required")
    if not timestamps:
        raise ValueError("ERROR: workbook_name input must end with '.xlsx'")
    if not "/" in filepath:
        raise ValueError("ERROR: file path is not a path")
    
    SortedID = namedtuple("SortedID", ["provenance_id", "project_path", "confidence", "extra", "why"])

    folders = filepath.split("/")
    final_path = filepath

    # Name follows prescribed naming structure
    if folders[1].isdigit() and len(folders[1]) == 3:
        base_path = './' + folders[1]
        final_path = os.path.relpath(filepath, base_path)
        id = folders[1]
        path = final_path
        confidence = 3
        extra = "Path robust, high confidence in project ID "
        why = "Follows prescribed naming structure"
    elif ".im" in folders[1]:
        id = folders[1][23:27]
        path = final_path
        confidence = 3
        extra = "Path robust, high confidence in project ID "
        why = "Follows prescribed naming structure"
    elif " " in folders[1]:
        for i in folders[1].split(" "):
            if i.isdigit() and len(i) == 3:
                id = i
                confidence = 3
            else:
                id = folders[1].split(" ")[0]
                confidence = 2
        path = final_path
        extra = "Path robust, high confidence in project ID "
        why = "Follows prescribed naming structure"
    elif len(extract_three_digits_after_240(filepath)) >= 1:
        id = extract_three_digits_after_240(filepath)[0]
        path = final_path
        confidence = 3
        extra = "Path robust, high confidence in project ID "
        why = "Follows prescribed naming structure"
    elif ".im" in folders[-1]:
        id = folders[1][23:27]
        path = final_path
        confidence = 2
        extra = "Path robust, project ID moderate confidence"
        why = "Project ID moderate confidence, robust path"
    elif len(extract_three_digit_numbers(filepath)) >= 1:
        id = (extract_three_digit_numbers(filepath))[0]
        path = final_path
        confidence = 3
        extra = "Path robust, high confidence in project ID "
        why = "Distinct project ID in path"
    elif len(extract_three_digits_after_230(filepath)) >= 1:
        id = extract_three_digits_after_230(filepath)[0]
        path = final_path
        confidence = 2
        extra = "Path robust, moderate confidence in project ID "
        why = "Follows prescribed naming structure"
    elif len(extract_three_digits_after_20190(filepath)) >= 1:
        id = extract_three_digits_after_20190(filepath)[0]
        path = final_path
        confidence = 2
        extra = "Path robust, moderate confidence in project ID "
        why = "Follows prescribed naming structure"
    else:
        id = None
        path = final_path
        confidence = 0
        extra = "Path not robust, no project ID "
        why = "No ID found, path unknown"


    return SortedID(provenance_id=id,project_path=path, confidence=confidence, extra=extra, why=why)