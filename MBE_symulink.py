import os 
import re
from collections import namedtuple

def extract_three_digit_numbers(path):
    return re.findall(r'(?<!\d)\d{3}(?!\d)', path)

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
    file = folders[-1]
    parts = file.split("_")

    if len(folders) > 2:
        if folders[1].isdigit() and len(folders[2]) == 6:
            base_path = './' + folders[1] + '/' + folders[2]
            final_path = os.path.relpath(filepath, base_path)
        else:
            final_path = filepath
    else:
        final_path = filepath

    # Apparent MBE naming structure:
    # PDC_MBE316GM1_20250108_4_321_(SnWO4_109).zip
    # PDC == lab
    # MBE316GM1 == instrument
    # 20250108 == Date
    # 4 == run # for a date
    # 321 == project number 
    # (SnWO4_109) == material

    if len(parts) >= 5 and parts[4].isdigit() and len(parts[4]) == 3:
        id = parts[4]
        path = final_path
        confidence = 3
        extra = "Path robust, high confidence in project ID "
        why = "Follows prescribed naming structure"
    elif len(parts) >= 5 and  parts[4].isdigit() and len(parts[4]) != 3:
        id = None
        path = final_path
        confidence = 1
        extra = "Path robust, no project ID "
        why = "Follows prescribed naming structure, project ID not correct"
    elif extract_three_digit_numbers(filepath):
        ids = extract_three_digit_numbers(filepath)
        if ids[0] == '316' and len(ids) > 1:
            id = ids[1]
            path = final_path
            confidence = 2
            extra = "Path not robust, project ID "
            why = "Exactly 3 digit number found, assumed to be project ID"
        elif ids[0] == '316' and len(ids) <= 1:
            id = None
            path = final_path
            confidence = 1
            extra = "Path not robust, no project ID "
            why = "No project ID found, path not robust"
        else:
            id = ids[0]
            path = final_path
            confidence = 2
            extra = "Path not robust, project ID "
            why = "Exactly 3 digit number found, assumed to be project ID"
    else:
        id = None
        path = final_path
        confidence = 0
        extra = "Path not robust, no project ID "
        why = "Does not follow prescribed naming structure, project ID not correct"
        
    return SortedID(provenance_id=id,project_path=path, confidence=confidence, extra=extra, why=why)