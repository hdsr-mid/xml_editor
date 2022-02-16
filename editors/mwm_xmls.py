from editors.constants import INPUT_DIR
from editors.constants import OUTPUT_DIR
from editors.utils import get_progress_mapper
from lxml import etree as ET  # noqa
from path_finder import FileFinder
from pathlib import Path
from typing import List

import logging
import os


logger = logging.getLogger(__name__)


class MWM:
    @classmethod
    def get_file_paths(cls):
        file_finder = FileFinder(
            single_start_dir=INPUT_DIR,
            # multi_start_dir=[INPUT_DIR / "2019-09", INPUT_DIR / "2015-12"],
            extension=".xml",
            limit_depth=False,
            filename_regex="^[0-9]{14}_HDSR_",
        )
        logger.info(f"found {len(file_finder.paths)} paths")
        return file_finder.paths

    @classmethod
    def get_xml_tree(cls, _path: Path) -> ET.ElementTree:
        _tree = ET.parse(source=_path.as_posix())
        return _tree

    @classmethod
    def remove_namespace_from_tree(cls, tree: ET.ElementTree):
        for element in tree.iter():
            prefix, has_namespace, postfix = element.tag.partition("}")
            if has_namespace:
                element.tag = postfix  # strip all namespaces
        return tree

    @classmethod
    def edit_xmls(cls, xml_paths: List[Path]):
        progress_mapper = get_progress_mapper(nr_file_paths=len(xml_paths), progress_step=1)
        for file_index, _path in enumerate(xml_paths):
            is_empty_file = os.stat(_path).st_size == 0
            if is_empty_file:
                logger.warning(f"skipping empty xml: {_path}")
                continue
            tree = cls.get_xml_tree(_path=_path)
            if not tree:
                continue

            tree = cls.remove_namespace_from_tree(tree=tree)

            for elem in tree.iter():
                if elem.tag not in ("{http://www.wldelft.nl/fews/PI}event", "event"):
                    continue
                if "comment" in elem.attrib:
                    # empty comment field
                    elem.attrib["comment"] = ""
                # add flagsource
                elem.attrib["flagsource"] = "UR"
                # alphabetically sort comment keys
                new_data = dict(sorted(elem.attrib.items()))
                elem.attrib.clear()
                for key, value in new_data.items():
                    elem.attrib[key] = value

            # change dir (to new output dir) in path
            new_filename = Path(_path.as_posix().replace(INPUT_DIR.as_posix(), OUTPUT_DIR.as_posix()))

            if file_index in progress_mapper:
                logger.info(f"progress {progress_mapper[file_index]}%")

            yield new_filename, tree

    @classmethod
    def create_xml(cls, new_filename: Path, tree: ET.ElementTree) -> None:
        directory = new_filename.parent
        if not directory.is_dir():
            os.mkdir(directory)
        tree.write(file_or_filename=new_filename, encoding="UTF-8", xml_declaration=True)

    @classmethod
    def run_mwm(cls) -> None:
        _paths = cls.get_file_paths()
        edited_xmls = cls.edit_xmls(xml_paths=_paths)
        for new_filename, tree in edited_xmls:
            cls.create_xml(new_filename=new_filename, tree=tree)
