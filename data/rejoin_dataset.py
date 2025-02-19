import os
import glob

def join_files(original_file_path):
    file_name = os.path.basename(original_file_path)
    file_dir = os.path.dirname(original_file_path)
    part_prefix = os.path.join(file_dir, file_name + "_part_*")
    
    parts = sorted(glob.glob(part_prefix), key=lambda x: int(x.split("_part_")[-1]))

    with open(original_file_path, 'wb') as output_file:
        for part in parts:
            with open(part, 'rb') as chunk_file:
                output_file.write(chunk_file.read())
            print(f"Rejoined: {part}")

    print(f"Reconstruction complete! File saved as {original_file_path}")


join_files("data/glove.twitter.27B.100d.txt")
join_files("data/train.csv")
