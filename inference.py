import subprocess

# Define the terminal command you want to run
command = "ls -l"  # Example command, lists files in the current directory

# Run the command
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Print the output
print("Output:", result.stdout)

# Check if there was an error
if result.returncode != 0:
    print("Error:", result.stderr)
