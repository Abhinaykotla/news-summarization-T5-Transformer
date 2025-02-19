import os
import hashlib

def split_file(input_file, chunk_size=45*1024*1024):  # 45MB default
    # Create output directory
    base_name = os.path.basename(input_file)
    output_dir = f"{base_name}_split"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create manifest file
    manifest = {
        "original_file": base_name,
        "chunks": [],
        "total_size": os.path.getsize(input_file)
    }
    
    # Split file
    part_num = 1
    with open(input_file, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
                
            # Calculate hash
            sha256 = hashlib.sha256(chunk).hexdigest()
            
            # Write chunk
            part_name = f"{base_name}.part{part_num:03d}"
            part_path = os.path.join(output_dir, part_name)
            with open(part_path, "wb") as chunk_file:
                chunk_file.write(chunk)
            
            # Update manifest
            manifest["chunks"].append({
                "part": part_name,
                "sha256": sha256,
                "size": len(chunk)
            })
            
            part_num += 1
    
    # Save manifest
    manifest_path = os.path.join(output_dir, "manifest.sha256")
    with open(manifest_path, "w") as mf:
        mf.write(f"Original: {manifest['original_file']}\n")
        mf.write(f"Total Size: {manifest['total_size']}\n")
        for chunk in manifest["chunks"]:
            mf.write(f"{chunk['part']}|{chunk['sha256']}|{chunk['size']}\n")
    
    print(f"Split complete! {part_num-1} parts created in '{output_dir}'")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Split large files into chunks')
    parser.add_argument('input_file', help='File to split')
    parser.add_argument('-s', '--size', type=int, default=45,
                      help='Chunk size in megabytes (default: 45)')
    args = parser.parse_args()
    
    split_file(args.input_file, chunk_size=args.size*1024*1024)