import subprocess

def send_notification(message, title="Notification Title"):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

# Example usage
send_notification("Your message here", "Custom Title")
