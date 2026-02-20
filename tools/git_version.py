import subprocess
import os
from datetime import datetime

Import("env")

def get_app_version():
    # 1. Check for environment variable (GitHub Actions)
    version = os.environ.get("APP_VERSION")
    if version:
        return version
    
    # 2. Try to get git hash (Local)
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip().decode("utf-8")
    except Exception:
        return "dev"

version = get_app_version()
date = datetime.now().strftime("%b %d %Y")

print(f"\n--- [VERSION GENERATOR] Version: {version}, Date: {date} ---\n")

# Generate version.h file
include_dir = os.path.join(env.subst("$PROJECT_DIR"), "include")
if not os.path.exists(include_dir):
    os.makedirs(include_dir)

version_h_path = os.path.join(include_dir, "version.h")
with open(version_h_path, "w") as f:
    f.write("// Generated file - do not edit\n")
    f.write(f'#define APP_VERSION "{version}"\n')
    f.write(f'#define BUILD_DATE "{date}"\n')
