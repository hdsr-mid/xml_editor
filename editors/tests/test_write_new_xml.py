from editors.constants import BASE_DIR
from editors.mwm_xmls import MWM
from editors.tests.expected_xmls_str import expected1
from editors.tests.expected_xmls_str import expected2

import xml.etree.ElementTree as ET  # noqa


mapper = {
    "20151215104633_HDSR_PS1313_Waterlevel": expected1,
    "20210601151504_HDSR_PS2220_Waterlevel": expected2,
}


def test_new_mwm_xml_has_no_namespace():
    xml_1 = BASE_DIR / "tests" / "input" / "20151215104633_HDSR_PS1313_Waterlevel.xml"
    xml_2 = BASE_DIR / "tests" / "input" / "20210601151504_HDSR_PS2220_Waterlevel.xml"
    assert xml_1.is_file() and xml_2.is_file()
    new_a = MWM.edit_xmls(xml_paths=[xml_1, xml_2])
    for new_filename, tree in new_a:
        root = tree.getroot()
        xml_str = ET.tostring(element=root, encoding="UTF-8", method="xml")
        expected_xml_str = mapper[new_filename.stem]
        assert xml_str == expected_xml_str
