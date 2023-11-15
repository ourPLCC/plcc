## 1. Install Docker Desktop for your operating system.

* https://docs.docker.com/desktop/install/windows-install/
* https://docs.docker.com/desktop/install/mac-install/
* https://docs.docker.com/desktop/install/linux-install/

## 2. Run Docker Docker if it's not already running.

## 3. Start a shell with your code.

On Windows, open a command prompt (e.g., Start menu -> type `cmd`), and position it in the directory where you want to work. Then run the following.

```bash
docker run -it --rm -v "%cd%:/code" -w /code ghcr.io/ourplcc/plcc:latest
```

On MacOS or Linux, open a terminal running a standard shell (e.g., bash, zsh, etc), and position it in the directory where you want to work. Then run the following

```bash
docker run -it --rm -v "$PWD:/code" -w /code  ghcr.io/ourplcc/plcc:latest
```

## 4. Use PLCC inside the container.

Now you are inside a bash shell, positioned in /code, within Alpine linux, with PLCC and its dependencies installed, and the current directory (/code) contains all your code. You can now use all of PLCC's commands.

Feel free to use your favorite editor on your host machine to edit files.

## 5. `exit` when done.

When you are done, type `exit`. All the files you generated will be in your current working directory and its subdirectories.

