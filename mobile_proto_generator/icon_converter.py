import os
import struct

def convert_png_to_ico(png_path: str, ico_path: str):
    """
    Converts a standard PNG file to a Windows ICO file
    in pure Python without any external library dependencies.
    """
    if not os.path.exists(png_path):
        print(f"[Icon] Source PNG not found: {png_path}")
        return False

    try:
        with open(png_path, "rb") as f:
            png_data = f.read()

        png_size = len(png_data)

        # ICO Header: Reserved (0), Type (1 for ICO), Count (1 image)
        header = struct.pack("<HHH", 0, 1, 1)

        # Directory Entry:
        # Width (1 byte, 0 means 256px), Height (1 byte, 0 means 256px)
        # Colors (1 byte, 0), Reserved (1 byte, 0)
        # Planes (2 bytes, 1), Bits Per Pixel (2 bytes, 32)
        # Size of PNG (4 bytes), Offset of PNG (4 bytes, 6 bytes header + 16 bytes directory = 22)
        directory = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, png_size, 22)

        with open(ico_path, "wb") as f_out:
            f_out.write(header)
            f_out.write(directory)
            f_out.write(png_data)

        print(f"[Icon] Successfully created native icon: {ico_path}")
        return True
    except Exception as e:
        print(f"[Icon] Conversion error: {e}")
        return False

if __name__ == "__main__":
    convert_png_to_ico("logo.png", "logo.ico")
