# Native PLCC Installation

> Version 2.0.0 or above

See [Dependencies](Dependencies) for supported versions of Java, Python, and shells.

1. You need Command Prompt (on Windows) or a Bash shell to run PLCC's scripts.
2. Install Java JDK 11 or higher. We recommend [OpenJDK](https://openjdk.java.net/).
  * Ensure `java` and `javac` are in your PATH environment variable and are available from your shell. If not add the folder that contains `java` and `javac` to your PATH environment variable.
  * Ensure `java --version` and `javac --version` report the same version. If not, in the PATH environment variable, move the folder containing `java` and `javac` to the front of your PATH.
3. Install Python 3.8 or higher
  * Ensure `python` is in your PATH and available in your shell. If not, add the folder containing python to your PATH.
  * Ensure `python --version` reports the version of Python you installed. If not, you may need to adjust your PATH.
    * You may need to try `python3` or `py` depending on your operating system.
4. Download a copy of PLCC. You can do this in two different ways.
  1. Use git to clone https://github.com/ourPLCC/plcc into its new home, and checkout the tag for the version you want to use.
     ```bash
     git clone https://github.com/ourPLCC/plcc.git
     cd plcc
     git checkout v3.1.0
     ```
  2. Download a zip of the desired version of PLCC from the [PLCC Releases page](https://github.com/ourPLCC/plcc/releases), and extract it into its new home on your computer.
5. Identify the PLCC's `src` directory within the directory (or subdirectories) created when you extracted the zip.
6. Define a new environment variable named LIBPLCC whose value is the full path to PLCC's src directory.
7. Add the full path to PLCC's src directory to beginning of the PATH environment variable.

# Upgrading

## Via Git

If you used git to download and install PLCC, checkout the tag for the new version you want to use. For example, in the root of the PLCC directory...

```bash
git checkout v4.0.0
```

Read the CHANGELOG to see if there is anything else you need to do to upgrade to the new version.

## Via Zip

If you downloaded and extracted a zip when you installed PLCC, download a zip for the new version. Then, either...

1. Replace the old version with the new one by deleting the existing folder and then extracting the new zip into the same location
2. Or, extract the new version into a different directory and then update environment variable's accordingly (PATH and PLCCLIB).

Read the CHANGELOG to see if there is anything else you need to do to upgrade to the new version.
