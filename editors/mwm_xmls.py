from path_finder import FileFinder
from pathlib import Path
from typing import Dict
from typing import List

import logging
import os
import xml.etree.ElementTree as ET


# TODO:
#  niets over timezone (zoals nu)
#  dailight saving time als tag
#  Timezone GMT+1 als tag


logger = logging.getLogger(__name__)

Q_DRIVE = Path("Q:/")
INPUT_DIR = Q_DRIVE / "WIS/MWM/fews_import/peilschalen"
OUTPUT_DIR = Q_DRIVE / "WIS/MWM/fews_import/peilschalen_20210901_110000_comment_flagsource_output"
BASE_DIR = Path(__file__).parent


def setup_logging():
    """Adds a configured stream handler to the root logger."""
    LOG_LEVEL = logging.INFO
    LOG_DATE_FORMAT = "%H:%M:%S"
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

    _logger = logging.getLogger()
    _logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOG_LEVEL)
    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)


def get_file_paths():
    file_finder = FileFinder(
        single_start_dir=INPUT_DIR,
        # multi_start_dir=[INPUT_DIR / "2019-09", INPUT_DIR / "2015-12"],
        extension=".xml",
        limit_depth=False,
        filename_regex="^[0-9]{14}_HDSR_",
    )
    logger.info(f"found {len(file_finder.paths)} paths")
    return file_finder.paths


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


def get_xml_tree(_path: Path) -> ET.ElementTree:
    _tree = ET.parse(source=_path)
    return _tree


def remove_namespace_from_tree(tree: ET.ElementTree):
    for element in tree.iter():
        prefix, has_namespace, postfix = element.tag.partition("}")
        if has_namespace:
            element.tag = postfix  # strip all namespaces
    return tree


def edit_xmls(xml_paths: List[Path]):
    progress_mapper = get_progress_mapper(nr_file_paths=len(xml_paths), progress_step=1)
    for file_index, _path in enumerate(xml_paths):
        is_empty_file = os.stat(_path).st_size == 0
        if is_empty_file:
            logger.warning(f"skipping empty xml: {_path}")
            continue
        tree = get_xml_tree(_path=_path)
        if not tree:
            continue

        tree = remove_namespace_from_tree(tree=tree)

        for elem in tree.iter():
            if elem.tag not in ("{http://www.wldelft.nl/fews/PI}event", "event"):
                continue
            if "comment" in elem.attrib:
                # empty comment field
                elem.attrib["comment"] = ""
            # add flagsource
            elem.attrib["flagsource"] = "UR"
            # alphabetically sort comment keys
            elem.attrib = dict(sorted(elem.attrib.items()))

        # change dir (to new output dir) in path
        new_filename = Path(_path.as_posix().replace(INPUT_DIR.as_posix(), OUTPUT_DIR.as_posix()))

        if file_index in progress_mapper:
            logger.info(f"progress {progress_mapper[file_index]}%")

        yield new_filename, tree


def create_xml(new_filename: Path, tree: ET.ElementTree) -> None:
    directory = new_filename.parent
    if not directory.is_dir():
        os.mkdir(directory)
    tree.write(file_or_filename=new_filename, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    setup_logging()
    _paths = get_file_paths()
    edited_xmls = edit_xmls(xml_paths=_paths)
    for new_filename, tree in edited_xmls:
        create_xml(new_filename=new_filename, tree=tree)
    logger.info("shutting down")
