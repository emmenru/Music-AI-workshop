import subprocess

def generate_requirements_txt(output_file="requirements.txt"):
    """
    Generate a clean requirements.txt file from the current Python environment.
    
    Parameters:
    output_file (str): The name of the output file (default is "requirements.txt")
    """
    # Run pip freeze to get the list of installed packages
    result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    # Filter out the messy output
    packages = [line.strip() for line in result.stdout.splitlines() if "@" not in line]
    
    # Write the clean list of packages to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(packages))
    
    print(f"Requirements file generated: {output_file}")

generate_requirements_txt(output_file="requirements.txt")