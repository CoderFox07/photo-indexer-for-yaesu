##########################################################################################
## Yaesu SD Card Picture Indexer
##
## AUTHOR / AUTOR: Aurelio DK5AD
## Copyright (C) 2025 Aurelio
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.
##
## DISCLAIMER / HAFTUNGSAUSSCHLUSS:
##   This script is provided "AS IS", without warranty of any kind.
##   Use at your own risk. The author assumes no liability for any damages
##   or data loss resulting from its use.
##
##   Dieses Skript wird "wie es ist" bereitgestellt, ohne jegliche Garantie.
##   Verwendung auf eigene Gefahr. Der Autor übernimmt keinerlei Haftung
##   für Schäden oder Datenverluste, die durch die Nutzung entstehen.
##
##
## ENGLISH:
## Synchronizes the picture database files on a Yaesu radio’s SD card with the actual
## contents of the /PHOTO folder. New images are indexed automatically, deleted images
## are removed from the database, and all entries are renumbered according to Yaesu’s
## file naming rules.
##
## HOW TO USE:
## 1. Configure your callsign and radio ID in the "USER CONFIGURATION" section below.
## 2. Save this script to the root directory of your Yaesu SD card.
## 3. Add or remove JPG images in the /PHOTO folder.
## 4. Run the script from the SD card’s root directory:
##      python3 yaesu_sd_photo_indexer.py
## 5. For full options and help, run:
##      python3 yaesu_photo_indexer.py -h
##
## DEUTSCH:
## Synchronisiert die Bild-Datenbankdateien auf einer Yaesu-SD-Karte mit dem aktuellen
## Inhalt des /PHOTO-Ordners. Neue Bilder werden automatisch indexiert, gelöschte Bilder
## aus der Datenbank entfernt und alle Einträge nach Yaesu-Namenskonvention neu nummeriert.
##
## ANWENDUNG:
## 1. Trage dein Rufzeichen und deine Radio-ID im Abschnitt "BENUTZERKONFIGURATION" ein.
## 2. Speichere dieses Skript ins Hauptverzeichnis der Yaesu-SD-Karte.
## 3. Füge JPG-Bilder zum /PHOTO-Ordner hinzu oder lösche welche.
## 4. Starte das Skript im Hauptverzeichnis der SD-Karte:
##      python3 yaesu_photo_indexer.py
## 5. Für alle Optionen und Hilfe:
##      python3 yaesu_photo_indexer.py -h
##########################################################################################

import struct
import os
import glob
import time
from time import gmtime, strftime
import re
import argparse
import sys

# =========================================================================
# === USER CONFIGURATION / BENUTZERKONFIGURATION ===
#
# PLEASE EDIT THESE VALUES! / BITTE DIESE WERTE BEARBEITEN!
#
# Set your callsign and the Radio ID of your transceiver for permanent use.
#
# Trage hier dein Rufzeichen und die Radio-ID deines Geräts für die
# dauerhafte Nutzung ein.
# =========================================================================
MY_CALLSIGN = ""  # Enter your callsign here
MY_RADIO_ID = ""  # Enter your Radio ID here
# =========================================================================

# --- Global Settings ---
MAX_FILE_SIZE_RECOMMENDED = 16000
IMAGE_PREFIX = "M"

# --- Helper Functions ---
def my_send_date_minimal(t):
    ts = strftime("%y%m%d%H%M%S", t)
    rbyte = []
    for x in range(int(len(ts)/2)):
        rbyte.append(int(ts[2*x:2*x+2],16))
    return bytes(rbyte)

def my_ascii_byte_minimal(s, length, pad_char=b'\xff'):
    b = s.encode('ascii', errors='replace')
    return b.ljust(length, pad_char)[:length]

def create_record(original_basename, filepath, radio_id, callsign):
    """Creates a single 128-byte record for an image file."""
    record = bytearray(128)
    now = gmtime()
    record[0:4] = b'\x00\x00\x00\x00'
    record[4:9] = my_ascii_byte_minimal(" ", 5, b'\x20')
    record[9:19] = my_ascii_byte_minimal("ALL", 10, b'\x20')
    record[19:25] = my_ascii_byte_minimal(" ", 6, b'\x20')
    record[25:30] = my_ascii_byte_minimal(radio_id, 5, b'\x20')
    record[30:40] = my_ascii_byte_minimal(callsign, 10, b'\xff')
    record[40:46] = my_ascii_byte_minimal(" ", 6, b'\x20')
    date_bytes = my_send_date_minimal(now)
    record[46:52] = date_bytes; record[52:58] = date_bytes; record[58:64] = date_bytes
    record[64:80] = my_ascii_byte_minimal(original_basename, 16, b'\x20')
    filesize = os.path.getsize(filepath)
    record[80:84] = struct.pack('>l', filesize)
    record[84:100] = my_ascii_byte_minimal("TEMP_FILENAME.JPG", 16, b'\xff') # Placeholder
    record[100:120] = b'\xff' * 20
    record[120:128] = b'\x30\x20\x20\x20\x20\x20\x20\x20'
    return record

def main(args):
    print("======================================================================")
    print("=== Yaesu      Picture Indexer                                     ===")
    print("======================================================================")
    print("Author: Aurelio  |  Callsign: DK5AD\n")
    print("Licensed under GNU AGPL v3 - No warranty, use at your own risk.")
    
    input("Press Enter to continue, acknowledging use at your own risk...")

    # --- Phase 1: Pre-flight checks ---
    print("\n[1] Performing pre-flight checks...")
    print(f"  - Configuration OK (Callsign: {args.callsign}, Radio ID: {args.radioid})")
    
    script_path = os.path.dirname(os.path.realpath(__file__))
    qsolo_dir = os.path.join(script_path, "QSOLOG")
    photo_dir = os.path.join(script_path, "PHOTO")

    if not (os.path.isdir(qsolo_dir) and os.path.isdir(photo_dir)):
        print("\nERROR: The 'QSOLOG' and 'PHOTO' directories were not found.")
        print("Please ensure this script is in the root directory of the SD card.")
        exit(1)
    print("  - Directories 'QSOLOG' and 'PHOTO' found.")

    qsomng_path = os.path.join(qsolo_dir, "QSOMNG.dat")
    if not os.path.exists(qsomng_path):
        print("\nERROR: The master database file 'QSOLOG/QSOMNG.dat' is missing.")
        print("This file is essential for reading the radio's counters and is created during formatting.")
        print("\nACTION REQUIRED:")
        print("Please format the SD card in your Yaesu radio, then run this script again.")
        exit(1)
    print("  - Master database 'QSOMNG.dat' found.")

    # --- Phase 2: Analyze and Reconcile ---
    print("\n[2] Analyzing and reconciling files with database...")
    qsopctdir_path = os.path.join(qsolo_dir, "QSOPCTDIR.dat")
    db_record_map = {}
    if os.path.exists(qsopctdir_path):
        with open(qsopctdir_path, "rb") as f:
            while record := f.read(128):
                if len(record) == 128:
                    filename = record[84:100].strip(b'\xff\x00').decode('ascii', 'ignore')
                    if filename: db_record_map[filename] = record
    
    disk_files_set = {os.path.basename(p) for p in glob.glob(os.path.join(photo_dir, "*.[Jj][Pp][Gg]"))}
    db_filenames_set = set(db_record_map.keys())
    
    deleted_db_entries = db_filenames_set - disk_files_set
    if deleted_db_entries:
        for filename in sorted(list(deleted_db_entries)):
            print(f"  - Deleting DB entry for missing file: {filename}")
            
    files_to_add_or_recreate = disk_files_set - db_filenames_set
    final_image_data = []
    for filename in sorted(list(db_filenames_set.intersection(disk_files_set))):
        final_image_data.append({'original_basename': db_record_map[filename][64:80].strip(b' \xff\x00').decode('ascii', 'ignore'),
                                 'filepath': os.path.join(photo_dir, filename),
                                 'record': db_record_map[filename]})
    for filename in sorted(list(files_to_add_or_recreate)):
        filepath = os.path.join(photo_dir, filename)
        filesize = os.path.getsize(filepath)
        if filesize > MAX_FILE_SIZE_RECOMMENDED:
            print("  -----------------------------------------------------------------")
            print(f"  *** WARNING: Image file '{filename}' is large! ({filesize / 1024:.1f} KB)")
            print(f"  ***          Files over {MAX_FILE_SIZE_RECOMMENDED / 1024:.0f} KB may fail to download from Wires-X nodes")
            print(f"  ***          to certain radios like the Yaesu FT-5D.")
            print("  -----------------------------------------------------------------")
        final_image_data.append({'original_basename': filename,
                                 'filepath': filepath,
                                 'record': create_record(filename, filepath, args.radioid, args.callsign)})
    
    if not deleted_db_entries and not files_to_add_or_recreate:
        print("  - Database is already in sync with the PHOTO folder. Nothing to do.")
        exit(0)

    # --- Phase 3: Rebuild and Re-number ---
    print(f"\n[3] Rebuilding database for {len(final_image_data)} total images...")
    final_records_to_write = []
    temp_rename_suffix = ".rebuild_tmp"
    final_image_data.sort(key=lambda item: item['original_basename'])
    
    for item in final_image_data:
        if os.path.exists(item['filepath']):
            try:
                os.rename(item['filepath'], item['filepath'] + temp_rename_suffix)
                item['filepath'] += temp_rename_suffix
            except OSError as e:
                print(f"  - ERROR during temporary rename of {os.path.basename(item['filepath'])}: {e}")

    for index, item in enumerate(final_image_data):
        pctnum = index + 1
        new_generated_filename = f"{IMAGE_PREFIX}{args.radioid}{pctnum:06d}.jpg"
        new_filepath = os.path.join(photo_dir, new_generated_filename)
        try:
            if os.path.exists(item['filepath']):
                os.rename(item['filepath'], new_filepath)
                print(f"  -> Processing '{item['original_basename']}' as picture #{pctnum}")
            else:
                print(f"  - WARNING: Source file for '{item['original_basename']}' disappeared. Skipping.")
                continue
        except Exception as e:
            print(f"  - ERROR renaming to {new_generated_filename}: {e}. Skipping.")
            continue
        new_record = bytearray(item['record'])
        new_record[84:100] = my_ascii_byte_minimal(new_generated_filename, 16, b'\xff')
        final_records_to_write.append(bytes(new_record))

    # --- Phase 4: Write final database files ---
    print("\n[4] Writing final database files...")
    try:
        qsopctfat_path = os.path.join(qsolo_dir, "QSOPCTFAT.dat")
        with open(qsopctdir_path, "wb") as fdir, open(qsopctfat_path, "wb") as ffat:
            for i, record in enumerate(final_records_to_write):
                fdir.write(record)
                fat_entry = 0x40000000 + (int(i / 2) * 0x100) + ((i % 2) * 0x80)
                ffat.write(struct.pack('>L', fat_entry))
        print(f"  - QSOPCTDIR.dat and QSOPCTFAT.dat rebuilt with {len(final_records_to_write)} entries.")
        with open(qsomng_path, "r+b") as fd:
            fd.seek(16)
            fd.write(struct.pack('>H', len(final_records_to_write)))
        print(f"  - Picture count in QSOMNG.dat updated to {len(final_records_to_write)}.")
    except (IOError, PermissionError) as e:
        print("\nFATAL FILE SYSTEM ERROR:")
        print(f"Could not write to the database files. Reason: {e}")
        print("Please check if the SD card is write-protected or has file system errors.")
        exit(1)
        
    print("\n======================================================================")
    print("=== Process completed successfully!                                ===")
    print("======================================================================")

if __name__ == "__main__":
    help_epilog = """
*** CONFIGURATION / KONFIGURATION ***

EN: To use this script, your callsign and radio ID must be configured.
    1. For permanent use (recommended): 
       Edit the MY_CALLSIGN and MY_RADIO_ID variables at the top of this script file.
    2. To override settings for a single run: 
       Use the command-line arguments shown below.

DE: Um dieses Skript zu nutzen, müssen das Rufzeichen und die Radio-ID konfiguriert werden.
    1. Für die dauerhafte Nutzung (empfohlen): 
       Bearbeiten Sie die Variablen MY_CALLSIGN und MY_RADIO_ID am Anfang dieser Skript-Datei.
    2. Um die Einstellungen für einen einzelnen Durchlauf zu überschreiben: 
       Nutzen Sie die unten gezeigten Kommandozeilen-Argumente.
"""

    parser = argparse.ArgumentParser(
        description='Yaesu Picture Indexer: Synchronizes the SD card picture database with the PHOTO folder.\n\nLicensed under GNU AGPL v3 - No warranty, use at your own risk.',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=help_epilog # Füge den Epilog zur Standard-Hilfe hinzu.
    )
    
    parser.add_argument('-c', '--callsign', default=MY_CALLSIGN, help='Your callsign.')
    parser.add_argument('-r', '--radioid', default=MY_RADIO_ID, help='Your radio ID (case-sensitive).')
    
    if len(sys.argv) == 1 and (not MY_CALLSIGN or not MY_RADIO_ID):
        parser.print_help()
        exit(0)
    
    args = parser.parse_args()
    
    main(args)
