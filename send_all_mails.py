import subprocess

def run_script(script_name):
    print(f"\n🚀 Running: {script_name}")
    subprocess.run(["python3", f"./scripts/{script_name}"])

def main():
    print("📬 Starting Surbhikunj VOICE Mail Automation...")

    # Send birthday mail to Surbhikunj members
    run_script("send_surbhikunj_birthday_mail.py")

    # Send special birthday mail
    run_script("send_special_birthday_mail.py")

    # Send reminder mail to group
    run_script("send_reminder_mail.py")

    print("\n✅ All mails processed.")

if __name__ == "__main__":
    main()