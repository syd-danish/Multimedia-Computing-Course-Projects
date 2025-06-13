import zlib,os

def compress_file(input_file, compressed_file):
    with open(input_file, 'rb') as f:
        file_data = f.read()
        compressed_data = zlib.compress(file_data, level=9)
        with open(compressed_file, 'wb') as cf:
            cf.write(compressed_data)
    print(f"Compressed '{input_file}' to '{compressed_file}'")

def decompress_file(compressed_file, output_file):
    with open(compressed_file, 'rb') as cf:
        compressed_data = cf.read()
        try:
            new_data = zlib.decompress(compressed_data)
            with open(output_file, 'wb') as f:
                f.write(new_data)
            print(f"Decompressed '{compressed_file}' to '{output_file}'")
        except zlib.error as error:
            print(f"decompression error: {error}")

def compare_files(og_file, decomp_file):
    with open(og_file, 'rb') as og, open(decomp_file, 'rb') as dcf:
        org_data = og.read()
        decomp_data = dcf.read()
        if org_data == decomp_data:
            print("compression and decompression were successful.")
        else:
            print("There appears to be an issue\n the given files do not match!\n")


input_file = 'input.txt'
compressed_file = 'compressed.cmp'
decompressed_file = 'decompressed.txt'

if not os.path.exists(input_file):
    print(f"Input file '{input_file}' not found.")
    exit()  

compress_file(input_file, compressed_file)
decompress_file(compressed_file, decompressed_file)
compare_files(input_file, decompressed_file)
input_size = os.path.getsize(input_file)
compressed_size = os.path.getsize(compressed_file)
compression_ratio = compressed_size / input_size
#if input_size > 0 else 0
print(f"Original File Size: {input_size} bytes")
print(f"Compressed File Size: {compressed_size} bytes")
print(f"Compression Ratio: {compression_ratio:.2%}")
