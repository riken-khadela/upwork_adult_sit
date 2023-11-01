

def close_every_chrome():
    import subprocess

    # Get the path to the Chrome executable using the `whereis` command.
    chrome_path = subprocess.check_output(["whereis", "google-chrome"]).decode().split()[1]

    # Create a new subprocess object.
    subprocess_object = subprocess.Popen(
        [chrome_path, "--tab-close"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for the subprocess to finish executing.
    subprocess_object.wait()

    # Check if the subprocess exited successfully.
    if subprocess_object.returncode != 0:
        # Handle the error.
        raise Exception("Failed to close Chrome tab.")
    
    
    
    