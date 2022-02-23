from pathlib import Path


Q_DRIVE = Path("Q:/")
INPUT_DIR = Q_DRIVE / "WIS/MWM/fews_import/peilschalen"
OUTPUT_DIR = Q_DRIVE / "WIS/MWM/fews_import/peilschalen_20210901_110000_comment_flagsource_output"
BASE_DIR = Path(__file__).parent.parent
TEST_INPUT_DIR = BASE_DIR / "editors" / "tests" / "input"


def check_constants():
    assert INPUT_DIR.is_dir()
    assert OUTPUT_DIR.is_dir()
    assert BASE_DIR.is_dir()
    assert TEST_INPUT_DIR.is_dir()
