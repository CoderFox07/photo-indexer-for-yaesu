# Yaesu Picture Indexer

This script intelligently synchronizes the picture database on a Yaesu radio's SD card, allowing you to use your own JPG images without the official camera microphone.


**English:**  
This script is an unofficial tool and is not endorsed, supported, or affiliated with Yaesu or any of its subsidiaries. It is provided "as-is" without any warranties. Use it at your own risk. The author is not responsible for any damage, data loss, or malfunction of your radio or SD card caused by using this script. You must comply with all applicable laws and regulations regarding radio operation and content transmission.

**Deutsch:**  
Dieses Skript ist ein inoffizielles, von der Community entwickeltes Werkzeug und wird nicht von Yaesu oder einem seiner Tochterunternehmen unterstützt, genehmigt oder vertrieben. Es wird ohne jegliche Garantie bereitgestellt und die Nutzung erfolgt auf eigene Gefahr. Der Autor übernimmt keine Haftung für Schäden, Datenverlust oder Fehlfunktionen deines Funkgeräts oder der SD-Karte, die durch die Verwendung dieses Skripts entstehen können. Du bist verpflichtet, alle geltenden Gesetze und Vorschriften bezüglich Funkbetrieb und Inhaltsübertragung einzuhalten.

## English Version

***

*A German version of this guide can be found below.*

*Eine deutsche Version dieser Anleitung befindet sich weiter unten.*

***

### What is this script for?

This script acts as an intelligent "Picture Indexer" for your Yaesu SD card. It allows you to add your own JPG images to the `/PHOTO` folder and makes them available for sending via C4FM, just as if they were taken with the official camera microphone.

### The Problem it Solves

Yaesu radios (like the FT-5D, FTM-400, etc.) cannot use image files that are simply copied to the SD card's `/PHOTO` folder. The radio's firmware requires corresponding entries in its database files (located in the `/QSOLOG` folder) to recognize, display, and transmit the images. While manually creating these database entries is technically possible, it is extremely cumbersome and impractical. This script automates this entire process for you.

### Quick Start Guide

#### 1. Configure the Script

Before the first use, you must configure your personal data in the script. Open the `yaesu_indexer.py` file in a text editor and enter your callsign and Radio ID in the "USER CONFIGURATION" section at the top.

**Example:**
```python
# === USER CONFIGURATION ===
MY_CALLSIGN = ""  # Enter your callsign here
MY_RADIO_ID = ""  # Enter your Radio ID here
```
> **Tip:** The Radio ID is specific to your device, which you can find in your radio's menu (often under `Setup` -> `GM` -> `Radio ID`).

Save the file. This configuration is permanent, so you only need to do this once.

#### 2. Prepare Your Images

Copy the JPG images you want to use into the `/PHOTO` folder on your SD card. Please ensure your images meet the following criteria for best results:

*   **Format:** Standard JPEG (`.jpg`).
*   **JPEG Type:** Use **Baseline (Standard)** JPEG. **Do not** use "Progressive" JPEG, as the radio cannot display these. When exporting from image editing software (like GIMP), make sure the "Progressive" option is disabled.
*   **Metadata:** Export your images **without any extra metadata** (like EXIF data, thumbnails, or color profiles) to ensure maximum compatibility.
*   **Resolution:** Supported resolutions are **320x240** or **160x120** pixels.
*   **File Size (Very Important!):**
    *   **For reliable transmission, especially for Wires-X downloads to certain devices like the Yaesu FT-5D, it is recommended to keep the file size below 16 KB.**
    *   Images larger than this may be viewable on the sending radio but can cause the receiving radio to freeze during a Wires-X download.

#### 3. Run the Script

Place the configured `yaesu_indexer.py` script in the root directory of your SD card. Connect the SD card to your computer, navigate to its root directory in a terminal or command prompt, and run the script:
```bash
python3 yaesu_indexer.py
```
The script will now automatically find your new images, rename them according to the Yaesu convention, and build or update the necessary database files. Your message and audio logs will remain untouched.

After the script has finished, you can eject the SD card and use it in your radio.

### Compatibility

This script was developed and thoroughly tested with a **Yaesu FT-5D**. However, as it is based on the file structure also used by other C4FM-capable Yaesu devices, it should also be compatible with other models like the **FT-3D, FTM-400D**, and similar radios.

***

## Deutsche Version

### Wofür ist dieses Skript?

Dieses Skript agiert als intelligenter "Picture Indexer" für deine Yaesu SD-Karte. Es ermöglicht dir, eigene JPG-Bilder in den `/PHOTO`-Ordner zu kopieren und sie für den Versand via C4FM nutzbar zu machen – so, als wären sie mit dem offiziellen Kameramikrofon aufgenommen worden.

### Das Problem, das es löst

Yaesu-Funkgeräte (wie das FT-5D, FTM-400 etc.) können Bilddateien, die einfach in den `/PHOTO`-Ordner der SD-Karte kopiert werden, nicht verwenden. Die Firmware des Funkgeräts benötigt entsprechende Einträge in ihren Datenbankdateien (im `/QSOLOG`-Ordner), um die Bilder erkennen, anzeigen und senden zu können. Diese Datenbankeinträge manuell zu erstellen ist zwar technisch möglich, aber extrem aufwendig und unpraktikabel. Dieses Skript automatisiert den gesamten Prozess für dich.

### Kurzanleitung

#### 1. Skript konfigurieren

Vor der ersten Nutzung musst du deine persönlichen Daten im Skript hinterlegen. Öffne die Datei `yaesu_indexer.py` in einem Texteditor und trage dein Rufzeichen und deine Radio-ID im oberen Bereich "USER CONFIGURATION" ein.

**Beispiel:**
```python
# === USER CONFIGURATION ===
MY_CALLSIGN = ""  # Trage hier dein Rufzeichen ein
MY_RADIO_ID = ""  # Trage hier deine Radio-ID ein
```
> **Tipp:** Die Radio-ID ist eine gerätespezifische, die du im Menü deines Funkgeräts findest (oft unter `Setup` -> `GM` -> `Radio ID`).

Speichere die Datei. Diese Konfiguration ist dauerhaft, du musst sie also nur einmal vornehmen.

#### 2. Bilder vorbereiten

Kopiere die JPG-Bilder, die du verwenden möchtest, in den `/PHOTO`-Ordner auf deiner SD-Karte. Bitte stelle für beste Ergebnisse sicher, dass deine Bilder die folgenden Kriterien erfüllen:

*   **Format:** Standard-JPEG (`.jpg`).
*   **JPEG-Typ:** Verwende **Baseline (Standard)** JPEG. Verwende **kein** "Progressive" JPEG, da das Funkgerät diese nicht darstellen kann. Achte beim Export aus einem Bildbearbeitungsprogramm (wie GIMP) darauf, dass die Option "Progressive" deaktiviert ist.
*   **Metadaten:** Exportiere deine Bilder **ohne zusätzliche Metadaten** (wie EXIF-Daten, Thumbnails oder Farbprofile), um maximale Kompatibilität zu gewährleisten.
*   **Auflösung:** Unterstützte Auflösungen sind **320x240** oder **160x120** Pixel.
*   **Dateigröße (Sehr wichtig!):**
    *   **Für eine zuverlässige Übertragung, insbesondere für Downloads von Wires-X auf bestimmte Geräte wie das Yaesu FT-5D, wird empfohlen, die Dateigröße unter 16 KB (16.384 Bytes) zu halten.**
    *   Größere Bilder können zwar auf dem sendenden Gerät angezeigt werden, können aber dazu führen, dass ein empfangendes FT-5D bei einem Wires-X-Download einfriert.

#### 3. Skript ausführen

Platziere die konfigurierte `yaesu_indexer.py`-Datei im Hauptverzeichnis deiner SD-Karte. Verbinde die SD-Karte mit deinem Computer, navigiere in einem Terminal oder einer Kommandozeile in das Hauptverzeichnis der Karte und führe das Skript aus:
```bash
python3 yaesu_indexer.py
```
Das Skript findet nun automatisch deine neuen Bilder, benennt sie gemäß der Yaesu-Konvention um und erstellt bzw. aktualisiert die notwendigen Datenbankdateien. Deine Nachrichten- und Audio-Logs bleiben dabei unberührt.

Nachdem das Skript fertig ist, kannst du die SD-Karte auswerfen und in deinem Funkgerät verwenden.

### Kompatibilität

Dieses Skript wurde mit einem **Yaesu FT-5D** entwickelt und intensiv getestet. Da es auf der Dateistruktur basiert, die auch von anderen C4FM-fähigen Yaesu-Geräten verwendet wird, sollte es ebenfalls mit anderen Modellen wie dem **FT-3D, FTM-400D** und ähnlichen Funkgeräten kompatibel sein.
