"""Restore legacy helper modules and the missing IPL deliveries dataset."""

from pathlib import Path
import sysconfig
from urllib.request import urlopen


SITE_PACKAGES = Path(sysconfig.get_paths()["purelib"])

DOWNLOADS = {
    Path("Deliveries.csv"): "https://raw.githubusercontent.com/Priyam219/IPL-DATA-ANALYSIS/main/deliveries.csv",
    SITE_PACKAGES / "thinkstats2" / "thinkstats2.py": "https://raw.githubusercontent.com/AllenDowney/ThinkStats2/master/code/thinkstats2.py",
    SITE_PACKAGES / "thinkplot" / "thinkplot.py": "https://raw.githubusercontent.com/AllenDowney/ThinkStats2/master/code/thinkplot.py",
}


def main() -> None:
    for path, url in DOWNLOADS.items():
        if path.exists():
            print(f"exists: {path}")
            continue

        print(f"download: {url} -> {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(urlopen(url, timeout=30).read())


if __name__ == "__main__":
    main()
