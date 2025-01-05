
import subprocess

def auto_commit_push(commit_message):
    """
    Automatically stages, commits, and pushes changes to the GitHub repository.

    Args:
        commit_message (str): A message describing the changes made in the commit.
    """
    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        # Push to the master branch
        subprocess.run(["git", "push", "origin", "master"], check=True)
        print("✅ Changes committed and pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during git operation: {e}")
    