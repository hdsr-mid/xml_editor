from typing import Dict


def get_progress_mapper(nr_file_paths: int, progress_step: int) -> Dict[int, int]:
    """Map file_index to a progress percentage [0-100] with (file_index / total_number_files * 100)
    Example:
        input:
            nr_xml_file_paths = 12
            log_stepsize = 2
        output: {file_index: percentage}
            {3: 25, 6: 50, 9: 75, 12: 100}
    """
    assert isinstance(nr_file_paths, int)
    assert 0 < progress_step < 100, "please use a progress_step between 0 and 100"
    # start=0, end=101 to make sure 100% is also logged
    percentages = [x for x in range(0, 101, progress_step)]
    mapper = {(percentage / 100 * nr_file_paths) - 1: percentage for percentage in sorted(percentages)}
    return {round(k): v for k, v in mapper.items() if k >= 0}
