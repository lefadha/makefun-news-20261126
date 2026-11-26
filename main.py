"""Write the entry image. The image is in this repository; the program only has to
put those exact bytes at /output/entry.png, twice, with no network and no clock."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = Path("/output/entry.png")

OUT.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(ROOT / "entry.png", OUT)
print("wrote", OUT, OUT.stat().st_size, "bytes")
