import os

def split_file(file_path, chunk_size_mb=50):
    chunk_size = chunk_size_mb * 1024 * 1024
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    part_prefix = os.path.join(file_dir, file_name + "_part_")

    with open(file_path, 'rb') as f:
        part_num = 1
        while chunk := f.read(chunk_size):
            part_file = f"{part_prefix}{part_num}"
            with open(part_file, 'wb') as chunk_file:
                chunk_file.write(chunk)
            print(f"Created: {part_file}")
            part_num += 1

    print(f"Splitting complete! {part_num - 1} parts created.")


split_file("data/glove.twitter.27B.100d.txt")
split_file("data/train.csv")
