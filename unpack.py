#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


VITA_FOLDERS = {"app", "addcont", "patch", "license", "bgdl", "user", "psm"}


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def extract_zip(seven_zip, zip_path, dest_dir):
    log(f"-> Extracting {zip_path.name}...")
    subprocess.run(
        [seven_zip, "x", str(zip_path), f"-o{dest_dir}", "-y"],
        check=True,
        capture_output=True,
    )


def find_files(directory, extension):
    return list(Path(directory).rglob(f"*{extension}"))


def find_license_bin(temp_dir):
    bin_files = find_files(temp_dir, ".bin")
    for f in bin_files:
        if f.name != "eboot.bin":
            return f
    return None


def process_zip(seven_zip, pkg2zip_path, zip_path, output_dir, processed_dir):
    item_name = zip_path.stem
    is_dlc = "(dlc)" in item_name.lower()
    is_avatar = "(avatar)" in item_name.lower()

    type_str = "DLC" if is_dlc else "AVATAR" if is_avatar else "GAME"
    success = False

    log(f"\n{'='*60}")
    log(f"Processing [{type_str}]: {item_name}")
    log(f"{'='*60}")

    temp_dir = zip_path.parent / f"temp_{zip_path.name}"
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        extract_zip(seven_zip, zip_path, temp_dir)

        pkg_files = list(temp_dir.rglob("*.pkg"))
        if not pkg_files:
            log(f"-> ERROR: No .pkg file found inside {item_name}.")
            return

        pkg_file = pkg_files[0]
        pkg_dir = pkg_file.parent

        bin_file = find_license_bin(temp_dir)
        if bin_file:
            target_bin = pkg_dir / "work.bin"
            if bin_file != target_bin:
                log(f"-> Found license .bin. Moving next to .pkg and renaming to work.bin...")
                shutil.move(str(bin_file), str(target_bin))
        else:
            log("-> WARNING: No .bin license file found. Decryption may fail.")

        log(f"-> Decrypting and unpacking .pkg with pkg2zip...")
        subprocess.run(
            [str(pkg2zip_path), "-x", pkg_file.name],
            capture_output=True,
            cwd=str(pkg_dir),
        )

        log("-> Organizing decrypted files...")
        for folder in pkg_dir.iterdir():
            if folder.is_dir() and folder.name in VITA_FOLDERS:
                dest = output_dir / folder.name
                dest.mkdir(parents=True, exist_ok=True)
                for item in folder.iterdir():
                    if item.is_file():
                        shutil.copy2(str(item), str(dest / item.name))
                    else:
                        if (dest / item.name).exists():
                            shutil.rmtree(str(dest / item.name))
                        shutil.copytree(str(item), str(dest / item.name))

        log(f"-> SUCCESS: Finished processing {item_name}!")
        success = True

    finally:
        log("-> Cleaning up temporary files...")
        shutil.rmtree(str(temp_dir))

    if success:
        log("-> Archiving .zip to Processed_Zips folder...")
        shutil.move(str(zip_path), str(processed_dir / zip_path.name))


def main():
    parser = argparse.ArgumentParser(description="PS Vita .zip unpacker")
    parser.add_argument("zip_dir", help="Directory containing .zip files")
    parser.add_argument("--sevenzip", default="7z", help="Path to 7z executable")
    parser.add_argument("--pkg2zip", default="pkg2zip", help="Path to pkg2zip executable")
    args = parser.parse_args()

    pkg2zip_path = Path(args.pkg2zip)
    working_dir = Path(args.zip_dir)
    output_dir = working_dir / "ReadyForVita"
    processed_dir = working_dir / "Processed_Zips"

    if not shutil.which(args.sevenzip):
        log(f"[ERROR] 7-Zip not found at {args.sevenzip}.")
        return

    if not pkg2zip_path.exists() and not shutil.which(str(pkg2zip_path)):
        log(f"[ERROR] pkg2zip not found at {pkg2zip_path}.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    zip_files = list(working_dir.glob("*.zip"))

    if not zip_files:
        log("No new .zip files found in this directory.")
        return

    for zip_path in zip_files:
        process_zip(args.sevenzip, pkg2zip_path, zip_path, output_dir, processed_dir)

    log(f"\nAll operations completed!")


if __name__ == "__main__":
    main()
