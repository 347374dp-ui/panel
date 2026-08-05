# Mobile Proto Generator for Proxy (DP Panel)

A highly advanced, randomized Android device profile generator that serializes profiles into valid, new Protobuf messages and outputs them as hex strings. It includes direct integration with your DP Admin Control Panel's Firebase Realtime Database.

## Features

- **Realistic Device Templates:** Generates highly realistic device data for major brands: Google Pixel, Samsung Galaxy, Xiaomi, and OnePlus. Supports the newest flagship models such as the Galaxy S24 Ultra, Pixel 9 Pro XL, Xiaomi 14 Ultra, and OnePlus 12!
- **Randomized and Valid Parameters:** Uniquely randomizes device-specific parameters such as Android ID, MAC address, IMEI (validated using the Luhn algorithm), Serial Numbers, and Build fingerprint matching genuine mobile devices.
- **Dependency-Free Core:** Serialization to the standard Protobuf wire format is written from scratch in pure Python with no external dependencies (no need to install `protobuf`).
- **Direct Firebase Integration:** Automatically upload generated proto hex strings to your Firebase database (`/protos.json`) with a single command-line flag. Supports custom URLs and secure Auth Token / Database secrets.
- **Windows Batch Script:** Includes a user-friendly double-click `.bat` file to generate and upload protos interactively.

## File Structure

- `generator.py` - Core serialization engine and random device profile generator.
- `firebase_uploader.py` - Standard HTTP client helper to communicate with the Firebase Realtime Database.
- `main.py` - Command-line interface with various customization flags.
- `run_generator.bat` - Windows interactive batch launcher.
- `README.md` - Setup and usage guide.
- `requirements.txt` - Required package list (minimal / none required for offline use).

## Setup & Installation

Ensure you have Python 3 installed. Since the uploader and generator use standard Python libraries, you can run the generator offline or online out-of-the-box with **zero package installation**.

## How to Use

### Windows Users (Interactive Mode)
Simply double-click **`run_generator.bat`** to open the interactive menu! It will check your environment and let you generate, save, or upload mobile protos with a single keystroke.

### Command Line Mode
Navigate to the project directory:
```bash
cd mobile_proto_generator
```

#### 1. Generate and Display a Single Mobile Proto
Prints a randomized, serialized mobile proto hex string:
```bash
python3 main.py
```

#### 2. Generate and Print Full Device Profile Details
Print readable details of the generated profile (including Brand, Model, Fingerprint, IMEI, and Android ID) along with the hex string:
```bash
python3 main.py --details
```

#### 3. Generate Multiple Protos and Save to a File
Generate 10 mobile protos and save them as a JSON list of hex strings:
```bash
python3 main.py --count 10 --output generated_protos.json
```

If combined with `--details`, the JSON file will contain both the hex string and the complete readable device parameters for audit purposes:
```bash
python3 main.py --count 5 --details --output detailed_protos.json
```

#### 4. Upload Generated Protos Directly to Firebase
Generate 3 fresh mobile protos and upload them directly to your Firebase DB `/protos.json` node so that they are instantly available in the DP Admin Control Panel's Proto Pool:
```bash
python3 main.py --count 3 --upload
```

You can view the newly added custom protos instantly on the **UID Dashboard -> Proto Pool** section!

## Technical Specifications

- **Wire Type 0 (Varint):** Used for SDK versioning.
- **Wire Type 2 (Length-delimited):** Used for string attributes (Brand, Model, Android ID, Fingerprint, IMEI, Serial, Hardware, Board, etc.) ensuring robust and valid protobuf decoding.
