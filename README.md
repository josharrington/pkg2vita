# pkg2vita

**An automated tool to extract, decrypt, and organize PS Vita Games, DLCs, Updates, and Avatars.**

Processing PS Vita `.zip` files manually is tedious. **pkg2vita** automates the entire process: it extracts your `.zip` archives, routes and renames your license files, decrypts the `.pkg` packages, and organizes the output into Vita-ready folders (`app`, `addcont`, `patch`, `license`, etc.). All you have to do is drag and drop the final output to your memory card!

## Features

* **Batch Processing:** Drop as many `.zip` files as you want into the folder; the script will handle all of them in one go.
* **Smart Tracking:** Successfully processed `.zip` files are automatically moved to a `Processed_Zips` folder, meaning you can drop new games in later without wasting time re-processing old ones.
* **Smart Renaming & Routing:** Automatically finds your game's `.bin` license file (no matter how deeply it was nested in the zip), moves it next to the `.pkg`, and renames it to `work.bin` so the decryptor can read it.
* **Auto-Sorting:** Automatically sorts your decrypted files into Vita-native directories (`app/` for games, `addcont/` for DLCs, `license/` for avatars, `patch/` for updates).
* **Clean Cleanup:** Automatically deletes temporary extraction folders to save hard drive space.
* **Cross-platform:** Run via Docker or standalone Python — works on Linux, macOS, and Windows.

---

## Requirements

* **7-Zip** — Used for extracting the initial `.zip` files.
  * [7-zip.org](https://www.7-zip.org/)
  * Linux: `pacman -S 7zip` / `apt install p7zip-full` / `brew install p7zip`
* **pkg2zip** — The utility used to decrypt the Vita packages.
  * [pkg2zip releases on GitHub](https://github.com/mmozeiko/pkg2zip)
  * Arch Linux AUR: `pacman -S pkg2zip` (via AUR helper)
* **Python 3.7+** (for standalone use only)
* **Docker** (for Docker use only)

---

## Quick Start

### Docker (Recommended)

No manual dependencies needed — the Docker image bundles everything.

```bash
make build
make run ZIPDIR=/path/to/zip/directory
```

To use `podman` instead of `docker`, pass `ENGINE=podman`:

```bash
make ENGINE=podman build
make ENGINE=podman run ZIPDIR=/path/to/zip/directory
```

### Standalone Python

Install `7zip` and `pkg2zip` on your system, then run:

```bash
python unpack.py /path/to/zip/directory
```

---

## Setup & Installation

### Folder Structure

Create a new, empty folder and place your `.zip` files inside:

```
Vita Games/
  Game_1.zip
  Game_2_(DLC).zip
  Game_3_(Update).zip
  Game_4_(Avatar).zip
```

### Docker

```bash
make build
make run ZIPDIR=/path/to/zip/directory
```

To use `podman` instead of `docker`:

```bash
make ENGINE=podman build
make ENGINE=podman run ZIPDIR=/path/to/zip/directory
```

The script processes all `.zip` files in the directory. Output is written back to the same directory.

### Standalone Python

```bash
python unpack.py /path/to/zip/directory

# Optional: specify custom paths for 7z and pkg2zip
python unpack.py /path/to/zip/directory --sevenzip /usr/bin/7z --pkg2zip /usr/bin/pkg2zip
```

---

## The Output

Once the script finishes, it will generate a **`ReadyForVita`** folder with your files perfectly formatted, and move your original archives into a **`Processed_Zips`** folder.

```
Vita Games/
  Processed_Zips/  <-- Your original .zip files are safely stored here
  ReadyForVita/
    app/        <-- Contains your decrypted games (e.g., PCSB00550)
    addcont/    <-- Contains your decrypted DLCs
    patch/      <-- Contains game updates
    license/    <-- Contains Avatars and extra licenses
```

### Transferring to your PS Vita:

1. Connect your PS Vita to your PC using **VitaShell** (via USB or FTP) or by plugging your SD card directly into your PC (if using an SD2Vita adapter).
2. Open your main memory card directory (usually `ux0:`).
3. Copy the contents of the `ReadyForVita/` folder directly into the root of `ux0:` (or the root of your SD card).
   *(If prompted to merge folders, click **Yes**).*
4. Disconnect your Vita or reinsert your SD card.
5. In VitaShell, press **Triangle (△)** and select **"Refresh LiveArea"**.
6. Close VitaShell. Your games, DLCs, and updates will now appear as bubbles or be applied to your games on your home screen!

*(**Note:** Ensure you have the `NoNpDrm` plugin installed on your PS Vita, otherwise the games will give an error when launched).*
