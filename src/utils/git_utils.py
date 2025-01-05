# src/utils/git_utils.py

import subprocess
import logging

def auto_commit_push(commit_message):
    """
    Automatically commits and pushes changes to the Git repository.

    Args:
        commit_message (str): The commit message.

    Raises:
        subprocess.CalledProcessError: If Git commands fail.
    """
    try:
        logging.info("Staging changes for commit...")
        subprocess.run(["git", "add", "."], check=True)
        
        logging.info("Committing changes...")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        logging.info("Pushing to remote repository...")
        subprocess.run(["git", "push"], check=True)
        
        logging.info("Git commit and push completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Git command failed: {e}")
        raise
