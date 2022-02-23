from editors.constants import INPUT_DIR
from editors.constants import OUTPUT_DIR
from editors.utils import get_progress_mapper
from lxml import etree as lxml_etree
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
    def get_xml_tree(cls, _path: Path) -> lxml_etree.ElementTree:
        _tree = lxml_etree.parse(source=_path.as_posix())
        return _tree

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

            for elem in tree.iter():
                if elem.tag not in ("{http://www.wldelft.nl/fews/PI}event", "event"):
                    continue
                if "comment" in elem.attrib:
                    # empty comment field
                    elem.attrib["comment"] = ""
                # add flagSource
                elem.attrib["flagSource"] = "UR"
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
    def create_xml(cls, new_filename: Path, tree: lxml_etree.ElementTree) -> None:
        """
        # noqa
        When writing tree to .xml file we use xml_declaration=True. Why? read long explanation below:

        deze orig.xml (20151215104633_HDSR_PS1313_Waterlevel.xml)
        ----------------------------------------
        <?xml version="1.0" ?>
        <TimeSeries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
            <series>
                <header>
                    <type>instantaneous</type>
                    <locationId>PS1313</locationId>
                    <parameterId>h</parameterId>
                    <qualifierId>mcc</qualifierId>
                    <timeStep unit="nonequidistant" />
                    <startDate date="2015-12-15" time="10:46:37" />
                    <endDate date="2015-12-15" time="10:46:37" />
                    <missVal>NaN</missVal>
                    <sourceOrganisation>Mobile Water Management</sourceOrganisation>
                    <sourceSystem>DEV</sourceSystem>
                    <creationDate>2016-04-19</creationDate>
                    <creationTime>22:11:17</creationTime>
                </header>
                <event comment="https://ftp2.mobielwatermeten.nl/hdsr_photos/2015-12/20151215104637_HDSR_PS1313_Waterlevel.jpg" date="2015-12-15" flag="1" time="10:46:37" value="-2.100" />
            </series>
        </TimeSeries>
        ----------------------------------------
        wordt ingelezen met: >>> tree = lxml_etree.parse(source=xml_path.as_posix())
        en dan om te printen hier: >>> tree_string = lxml_etree.tostring(tree.getroot(), encoding='unicode', method='xml')
        # NOTE1: zonder .getroot() resulteert in dezelfde tree_string
        # NOTE2: encoding='utf-8' resulteert in bytes (geen str), maar zelfde content
        ----------------------------------------
        <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" version="1.2">
            <series>
                <header>
                    <type>instantaneous</type>
                    <locationId>None</locationId>
                    <parameterId>h</parameterId>
                    <qualifierId>mcc</qualifierId>
                    <timeStep unit="nonequidistant"/>
                    <startDate date="2015-12-15" time="08:58:20"/>
                    <endDate date="2015-12-15" time="08:58:20"/>
                    <missVal>NaN</missVal>
                    <sourceOrganisation>Mobile Water Management</sourceOrganisation>
                    <sourceSystem>DEV</sourceSystem>
                    <creationDate>2016-04-19</creationDate>
                    <creationTime>22:11:14</creationTime>
                </header>
                <event date="2015-12-15" time="08:58:20" value="0.530" flag="1" comment="http://hdsr01.mobilecanalcontrol.com/mcc/photolink/back/photoback_17242.jpg"/>
                </series>
        </TimeSeries>
        ----------------------------------------
        write xml to output_xml_1 file met xml_declaration=True
        new_filename = BASE_DIR / "output.xml"
        tree.write(file=new_filename.as_posix(), encoding="UTF-8", xml_declaration=True) --> default enconding='ASCII'
        ----------------------------------------
        <?xml version='1.0' encoding='UTF-8'?>
        <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" version="1.2">
            <series>
                <header>
                    <type>instantaneous</type>
                    <locationId>None</locationId>
                    <parameterId>h</parameterId>
                    <qualifierId>mcc</qualifierId>
                    <timeStep unit="nonequidistant"/>
                    <startDate date="2015-12-15" time="08:58:20"/>
                    <endDate date="2015-12-15" time="08:58:20"/>
                    <missVal>NaN</missVal>
                    <sourceOrganisation>Mobile Water Management</sourceOrganisation>
                    <sourceSystem>DEV</sourceSystem>
                    <creationDate>2016-04-19</creationDate>
                    <creationTime>22:11:14</creationTime>
                </header>
                <event date="2015-12-15" time="08:58:20" value="0.530" flag="1" comment="http://hdsr01.mobilecanalcontrol.com/mcc/photolink/back/photoback_17242.jpg"/>
            </series>
        </TimeSeries>
        ----------------------------------------
        write xml to output_xml_2 file met xml_declaration=False
        new_filename = BASE_DIR / "output.xml"
        tree.write(file=new_filename.as_posix(), encoding="UTF-8", xml_declaration=False) --> default encoding='ASCII'
        ----------------------------------------
        <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" version="1.2">
            <series>
                <header>
                    <type>instantaneous</type>
                    <locationId>None</locationId>
                    <parameterId>h</parameterId>
                    <qualifierId>mcc</qualifierId>
                    <timeStep unit="nonequidistant"/>
                    <startDate date="2015-12-15" time="08:58:20"/>
                    <endDate date="2015-12-15" time="08:58:20"/>
                    <missVal>NaN</missVal>
                    <sourceOrganisation>Mobile Water Management</sourceOrganisation>
                    <sourceSystem>DEV</sourceSystem>
                    <creationDate>2016-04-19</creationDate>
                    <creationTime>22:11:14</creationTime>
                </header>
                <event date="2015-12-15" time="08:58:20" value="0.530" flag="1" comment="http://hdsr01.mobilecanalcontrol.com/mcc/photolink/back/photoback_17242.jpg"/>
            </series>
        </TimeSeries>
        ----------------------------------------
        arguments when writing xml to file = tree.write(file, encoding=None, method="xml", pretty_print=False, xml_declaration=None, with_tail=True, standalone=None, doctype=None, compression=0, exclusive=False, inclusive_ns_prefixes=None, with_comments=True, strip_text=False): # real signature unknown; restored from __doc__)
        verschillen tussen orig, tree_string, output_xml_1 en output_xml_2:
        1) xml version
            - orig          heeft <?xml version="1.0" ?>
            - tree_string   heeft geen <?xml version="1.0" ?>
            - output_xml_1  heeft <?xml version='1.0' encoding='UTF-8'?>   <-- encoding erbij omdat xml_declaration=True
            - output_xml_2  heeft geen <?xml version="1.0" ?> <-- omdat xml_declaration=False
        2) TimeSeries tag
            - orig          <TimeSeries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
            - tree_string   <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" version="1.2">
            - output_xml_1  <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" version="1.2">
            - output_xml_2  <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" version="1.2">
            om beter te vergelijken gesorteerd obv orig volgorde:
            - orig          <TimeSeries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
            - tree_string   <TimeSeries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" xmlns="http://www.wldelft.nl/fews/PI">
            - output_xml_1  <TimeSeries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" xmlns="http://www.wldelft.nl/fews/PI">
            - output_xml_2  <TimeSeries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" xmlns="http://www.wldelft.nl/fews/PI">

        Deze orig.xml (20210601151504_HDSR_PS2220_Waterlevel.xml) (heeft andere indentation als eerder orig xml..)
        ----------------------------------------
        <?xml version="1.0" ?>
        <TimeSeries version="1.2" xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
          <series>
            <header>
              <type>instantaneous</type>
              <locationId>PS2220</locationId>
              <parameterId>h</parameterId>
              <qualifierId>mcc</qualifierId>
              <timeStep unit="nonequidistant"/>
              <startDate date="2021-06-01" time="15:00:39"/>
              <endDate date="2021-06-01" time="15:02:04"/>
              <missVal>-999</missVal>
              <sourceOrganisation>Mobile Water Management</sourceOrganisation>
              <sourceSystem>BES</sourceSystem>
              <creationDate>2021-06-01</creationDate>
              <creationTime>15:15:04</creationTime>
            </header>
            <event comment="https://ftp2.mobielwatermeten.nl/hdsr_photos/2021-06/20210601150039_HDSR_PS2220_Waterlevel.jpg" date="2021-06-01" flag="3" time="15:00:39" user="Aad Versteeg" value="-1.33"/>
            <event comment="https://ftp2.mobielwatermeten.nl/hdsr_photos/2021-06/20210601150204_HDSR_PS2220_Waterlevel.jpg" date="2021-06-01" flag="3" time="15:02:04" user="Aad Versteeg" value="-1.37"/>
          </series>
        </TimeSeries>
        ----------------------------------------
        wordt ingelezen met: >>> tree = lxml_etree.parse(source=xml_path.as_posix())
        en dan om te printen hier: >>> tree_string = lxml_etree.tostring(tree.getroot(), encoding='unicode', method='xml')
        # NOTE1: zonder .getroot() resulteert in dezelfde tree_string
        # NOTE2: encoding='utf-8' resulteert in bytes (geen str), maar zelfde content
        ----------------------------------------
        <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
          <series>
            <header>
              <type>instantaneous</type>
              <locationId>PS2220</locationId>
              <parameterId>h</parameterId>
              <qualifierId>mcc</qualifierId>
              <timeStep unit="nonequidistant"/>
              <startDate date="2021-06-01" time="15:00:39"/>
              <endDate date="2021-06-01" time="15:02:04"/>
              <missVal>-999</missVal>
              <sourceOrganisation>Mobile Water Management</sourceOrganisation>
              <sourceSystem>BES</sourceSystem>
              <creationDate>2021-06-01</creationDate>
              <creationTime>15:15:04</creationTime>
            </header>
            <event comment="https://ftp2.mobielwatermeten.nl/hdsr_photos/2021-06/20210601150039_HDSR_PS2220_Waterlevel.jpg" date="2021-06-01" flag="3" time="15:00:39" user="Aad Versteeg" value="-1.33"/>
            <event comment="https://ftp2.mobielwatermeten.nl/hdsr_photos/2021-06/20210601150204_HDSR_PS2220_Waterlevel.jpg" date="2021-06-01" flag="3" time="15:02:04" user="Aad Versteeg" value="-1.37"/>
          </series>
        </TimeSeries>
        ----------------------------------------
        write xml to output_xml_1 file met xml_declaration=True
        new_filename = BASE_DIR / "output.xml"
        tree.write(file=new_filename.as_posix(), encoding="UTF-8", xml_declaration=True) --> default enconding='ASCII'
        ----------------------------------------
        <?xml version='1.0' encoding='UTF-8'?>
        <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
          <series>
            <header>
              <type>instantaneous</type>
              <locationId>PS2220</locationId>
              <parameterId>h</parameterId>
              <qualifierId>mcc</qualifierId>
              <timeStep unit="nonequidistant"/>
              <startDate date="2021-06-01" time="15:00:39"/>
              <endDate date="2021-06-01" time="15:02:04"/>
              <missVal>-999</missVal>
              <sourceOrganisation>Mobile Water Management</sourceOrganisation>
              <sourceSystem>BES</sourceSystem>
              <creationDate>2021-06-01</creationDate>
              <creationTime>15:15:04</creationTime>
            </header>
            <event comment="https://ftp2.mobielwatermeten.nl/hdsr_photos/2021-06/20210601150039_HDSR_PS2220_Waterlevel.jpg" date="2021-06-01" flag="3" time="15:00:39" user="Aad Versteeg" value="-1.33"/>
            <event comment="https://ftp2.mobielwatermeten.nl/hdsr_photos/2021-06/20210601150204_HDSR_PS2220_Waterlevel.jpg" date="2021-06-01" flag="3" time="15:02:04" user="Aad Versteeg" value="-1.37"/>
          </series>
        </TimeSeries>
        ----------------------------------------
        write xml to output_xml_2 file met xml_declaration=False
        new_filename = BASE_DIR / "output.xml"
        tree.write(file=new_filename.as_posix(), encoding="UTF-8", xml_declaration=False) --> default encoding='ASCII'
        ----------------------------------------
        <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
          <series>
            <header>
              <type>instantaneous</type>
              <locationId>PS2220</locationId>
              <parameterId>h</parameterId>
              <qualifierId>mcc</qualifierId>
              <timeStep unit="nonequidistant"/>
              <startDate date="2021-06-01" time="15:00:39"/>
              <endDate date="2021-06-01" time="15:02:04"/>
              <missVal>-999</missVal>
              <sourceOrganisation>Mobile Water Management</sourceOrganisation>
              <sourceSystem>BES</sourceSystem>
              <creationDate>2021-06-01</creationDate>
              <creationTime>15:15:04</creationTime>
            </header>
            <event comment="https://ftp2.mobielwatermeten.nl/hdsr_photos/2021-06/20210601150039_HDSR_PS2220_Waterlevel.jpg" date="2021-06-01" flag="3" time="15:00:39" user="Aad Versteeg" value="-1.33"/>
            <event comment="https://ftp2.mobielwatermeten.nl/hdsr_photos/2021-06/20210601150204_HDSR_PS2220_Waterlevel.jpg" date="2021-06-01" flag="3" time="15:02:04" user="Aad Versteeg" value="-1.37"/>
          </series>
        </TimeSeries>
        ----------------------------------------
        arguments when writing xml to file = tree.write(file, encoding=None, method="xml", pretty_print=False, xml_declaration=None, with_tail=True, standalone=None, doctype=None, compression=0, exclusive=False, inclusive_ns_prefixes=None, with_comments=True, strip_text=False): # real signature unknown; restored from __doc__)
        verschillen tussen orig, tree_string, output_xml_1 en output_xml_2:
        1) xml version (zelfde verschillen als bij vorige orig xml (20151215104633_HDSR_PS1313_Waterlevel.xml)
        2) TimeSeries tag
            - orig          <TimeSeries version="1.2" xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
            - tree_string   <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
            - output_xml_1  <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" version="1.2">
            - output_xml_2  <TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
            om beter te vergelijken gesorteerd obv orig volgorde:
            - orig          <TimeSeries version="1.2" xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
            - tree_string   <TimeSeries version="1.2" xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
            - output_xml_1  <TimeSeries version="1.2" xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
            - output_xml_2  <TimeSeries version="1.2" xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
        """
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
