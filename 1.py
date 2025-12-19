# Read the contents of the requirements.txt file
file_path = r'\cloudide\workspace\Python\requirements.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# Initialize a dictionary to store package information
package_info = {}

# Parse each line to extract package name, version, and hashes
for line in lines:
    if line.strip():
        parts = line.split('==')
        package_name = parts[0]
        version_hash = parts[1].split(';')[0].strip()
        hashes = [hash_part.split('=')[1].strip() for hash_part in parts[1].split('--hash=')[1:]]
        package_info[package_name] = {'version': version_hash, 'hashes': hashes}

# Debugging: Print the extracted package information
for package, info in package_info.items():
    print(f"Package: {package}")
    print(f"Version: {info['version']}")
    print("Hashes:")
    for idx, hash_val in enumerate(info['hashes']):
        print(f"Hash {idx + 1}: {hash_val}")
    print()
