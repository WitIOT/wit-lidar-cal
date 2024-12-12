import struct

def debug_metadata(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()

    header_start = data.find(b"WAVEDESC")
    if header_start == -1:
        raise ValueError("WAVEDESC not found in the file")
    
    print(f"Header starts at byte: {header_start}")

    # Print raw data around header start for debugging
    print("Raw data near WAVEDESC (first 64 bytes):")
    print(data[header_start:header_start + 64])

    # Extract raw bytes for num_samples
    num_samples_raw = data[header_start + 60:header_start + 64]
    print(f"Raw bytes for num_samples: {num_samples_raw.hex()}")

    # Try reading num_samples in both Big-Endian and Little-Endian
    num_samples_be = struct.unpack(">i", num_samples_raw)[0]
    num_samples_le = struct.unpack("<i", num_samples_raw)[0]

    print(f"Number of Samples (Big-Endian): {num_samples_be}")
    print(f"Number of Samples (Little-Endian): {num_samples_le}")

# Example usage
debug_metadata("02.trc")  # Replace with your file path
