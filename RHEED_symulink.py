import os
from pathlib import Path

from common import SortedID, extract_three_digit_numbers, extract_three_digits_after

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
    folders = list(filepath.parts)
    final_path = str(filepath)

    # Name follows prescribed naming structure
    for i in folders:
        if i.isdigit() and len(i) == 3:
            base_path = './' + i
            id = i
            path = str(os.path.relpath(filepath, base_path))
            confidence = 3
            extra = "Path robust, high confidence in project ID "
            why = "Follows prescribed naming structure"
            return SortedID(provenance_id=id,project_path=path, confidence=confidence, extra=extra, why=why)
    if ".img" in folders[-1] and len(folders[-1]) == 57 and folders[-1][23:27].isdigit():
        id = folders[0][23:27]
        path = final_path
        confidence = 3
        extra = "Path robust, high confidence in project ID "
        why = "Follows prescribed naming structure"
    elif 'PARADIM' in str(filepath):
        for i in folders:
            if i[0:8] == 'PARADIM-':
                id = i[8:11]
                path = final_path
                confidence = 2
                extra = "Path found, probable project ID "
                why = "Probable project ID"
    elif " " in folders[1] and folders[1].split(" ")[0].isdigit() and len(folders[1].split(" ")[0]) == 3:
        id = folders[1].split(" ")[0]
        path = final_path
        confidence = 3
        extra = "Path found, project ID found"
        why = "Project ID and path found"
    else:
        id = None
        path = final_path
        confidence = 0
        extra = "Path not robust, no project ID "
        why = "No ID found, path unknown"

    return SortedID(provenance_id=id,project_path=path, confidence=confidence, extra=extra, why=why)

#Hanjong_CeO2_2024