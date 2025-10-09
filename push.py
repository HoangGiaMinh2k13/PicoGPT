import subprocess, os, time

def push_all_to_github():
    token = os.environ["GITHUB_TOKEN"]
    repo_url = os.environ["GITHUB_REPO"]

    # Inject token into repo URL for authentication
    authed_url = repo_url.replace("https://", f"https://{token}@")

    try:
        subprocess.run(["git", "config", "--global", "user.email", "render@bot.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "RenderBot"], check=True)

        # Stage all changes
        subprocess.run(["git", "add", "-A"], check=True)

        # Commit with timestamp
        subprocess.run(["git", "commit", "-m", f"Auto-update at {time.ctime()}"], check=True)

        # Push to main (or your branch)
        subprocess.run(["git", "push", authed_url, "main"], check=True)

        print("✅ All changes pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git push failed: {e}")