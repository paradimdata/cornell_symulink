import os
from pathlib import Path
from common import SortedID, extract_three_digit_numbers

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
    #    project_path : the path, excluding filename (or None), where this object should appear in the project data. 
    #                  e.g. "rheed1/02-28-2024" or "mbe/05-16-2025/Sample116" or None if unknown.
    #    confidence : integer representing the confidence in the assignment
    #                 e.g. 3=HIGH, 2=MEDIUM, 1=LOW, 0=NONE.
    #                 If HIGH, the other two parameters MUST NOT be None.
    # The returned object/tuple can contain other elements as well, but must contain these three.

    if not filepath:
        raise ValueError("ERROR: a file path is required")

    filepath = Path(filepath) # should already be a Path object, but just in case; note leading "./" are trimmed automatically by Path
    final_path = str(filepath)

    if len(extract_three_digit_numbers(filepath)) >= 1:
        id = extract_three_digit_numbers(filepath)[0]
        path = final_path
        confidence = 3
        extra = "Path robust, high confidence in project ID "
        why = "ID found, path expected to be robust"
    else:
        id = None
        path = final_path
        confidence = 0
        extra = "No ID found"
        why = "No ID found"

    return SortedID(provenance_id=id,project_path=path, confidence=confidence, extra=extra, why=why)
