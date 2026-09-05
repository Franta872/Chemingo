# this was built by ChatGPT because I don't want to bother with packaging

from pathlib import Path
import os
import platform
import shutil
import stat
import subprocess
import sys
import urllib.request


ROOT = Path(__file__).resolve().parent.parent
PACKAGING = ROOT / "packaging"
DIST = ROOT / "dist"
BUILD = ROOT / "build"


def run(*args, env=None):
    print(f"\n> {' '.join(map(str, args))}")
    subprocess.run(args, cwd=ROOT, env=env, check=True)


def clean():
    print("Cleaning previous build...")

    shutil.rmtree(BUILD, ignore_errors=True)
    shutil.rmtree(DIST, ignore_errors=True)

    DIST.mkdir(exist_ok=True)


def build_windows():
    print("Building Chemingo for Windows...")

    run(
        sys.executable,
        "-m",
        "PyInstaller",
        "packaging/Chemingo-Windows.spec",
    )

    print("\nBuild finished:")
    print(DIST / "Chemingo-Windows-x64.exe")


def build_linux():
    print("Building Chemingo for Linux...")

    run(
        sys.executable,
        "-m",
        "PyInstaller",
        "packaging/Chemingo-Linux.spec",
    )

    executable = DIST / "Chemingo-Linux-x64"

    appdir = PACKAGING / "appimage" / "AppDir"
    shutil.rmtree(appdir, ignore_errors=True)

    bin_dir = appdir / "usr" / "bin"
    applications_dir = appdir / "usr" / "share" / "applications"
    icons_dir = appdir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"

    bin_dir.mkdir(parents=True)
    applications_dir.mkdir(parents=True)
    icons_dir.mkdir(parents=True)

    shutil.copy2(executable, bin_dir / "Chemingo")

    icon_source = PACKAGING / "icons" / "Chemingo-icon.png"
    shutil.copy2(icon_source, icons_dir / "chemingo.png")
    shutil.copy2(icon_source, appdir / "chemingo.png")

    desktop = """[Desktop Entry]
Type=Application
Name=Chemingo
Comment=Chemistry quiz application
Exec=Chemingo
Icon=chemingo
Terminal=true
Categories=Education;
"""

    (appdir / "Chemingo.desktop").write_text(desktop)
    (applications_dir / "Chemingo.desktop").write_text(desktop)

    apprun = """#!/bin/sh

HERE="$(dirname "$(readlink -f "$0")")"

if [ -t 0 ]; then
    exec "$HERE/usr/bin/Chemingo"
else
    exec x-terminal-emulator -e "$HERE/usr/bin/Chemingo"
fi
"""

    apprun_path = appdir / "AppRun"
    apprun_path.write_text(apprun)

    apprun_path.chmod(
        apprun_path.stat().st_mode
        | stat.S_IXUSR
        | stat.S_IXGRP
        | stat.S_IXOTH
    )

    tools = PACKAGING / ".tools"
    tools.mkdir(exist_ok=True)

    appimagetool = tools / "appimagetool-x86_64.AppImage"

    if not appimagetool.exists():
        print("\nDownloading appimagetool...")

        urllib.request.urlretrieve(
            "https://github.com/AppImage/AppImageKit/releases/download/continuous/"
            "appimagetool-x86_64.AppImage",
            appimagetool,
        )

        appimagetool.chmod(
            appimagetool.stat().st_mode
            | stat.S_IXUSR
            | stat.S_IXGRP
            | stat.S_IXOTH
        )

    output = DIST / "Chemingo-Linux-x86_64.AppImage"

    env = os.environ.copy()
    env["ARCH"] = "x86_64"

    run(
        str(appimagetool),
        str(appdir),
        str(output),
        env=env,
    )

    output.chmod(
        output.stat().st_mode
        | stat.S_IXUSR
        | stat.S_IXGRP
        | stat.S_IXOTH
    )

    print("\nBuild finished:")
    print(output)


def main():
    clean()

    system = platform.system()

    if system == "Windows":
        build_windows()
    elif system == "Linux":
        build_linux()
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")


if __name__ == "__main__":
    main()

