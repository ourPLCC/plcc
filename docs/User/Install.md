# Install PLCC

This document will help you install PLCC into in your
preferred environment.

## 1. Quick Start

### 1.1. Bash

Requires bash, curl, Git, Java SDK >=11, and Python >=3.5.10.

```bash
/bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)"
```

After following the instructions printed by the last command,
test your installation
(see "Test your PLCC installation" at the end of this document.).

### 1.2. Docker

Start a shell in the PLCC container.

```bash
docker run --rm -it -v "${PWD}:/workdir" ghcr.io/ourplcc/plcc:latest
```

You can also run single commands in the PLCC container as follows.

```bash
docker run --rm -it -v "${PWD}:/workdir" ghcr.io/ourplcc/plcc:latest PLCC COMMAND HERE
```

Test your installation (see "Test your PLCC installation" at the end of
this document.)

### 1.3. GitPod

Add or update `.gitpod.yml` in the root of your GitLab/GitHub/Bitbucket
repository with the following:

```yaml
image: gitpod/workspace-full:latest

tasks:
  - name: Install PLCC
    command: |
        /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)" >> ~/.bashrc
        # Uncomment to checkout install specific version
        # git -C "$HOME/.local/plcc/" checkout v4.0.1
        exec bash
```

Open a new GitPod workspace for this repository and test your installation
(see "Test your PLCC installation" at the end of this document.)

## 1.4. If none of the above work for you...

Read on.

## 2. Install and Use PLCC

PLCC can be installed and used in different environments.
This section provides a brief guide to help you select the
environment best for you and your class.

### 2.1. Native Environment

One can install PLCC and its dependencies into a native, local environment.
PLCC depends on Java >= 11 and Python >= 3.5.10 and requires environment
variables to be set or modified. Once installed, one can use PLCC's commands
in either a Bash shell on Linux/maxOS or Windows, or a Command-Prompt
in Windows.

Advantages

* Each individual can choose the version of Python and Java PLCC uses.
* Each individual can use PLCC in an environment that they have customized
  to their personal tastes.

Disadvantages

* It is difficult to support students who may each have a different
  environment (hardware, OS, applications, shells, IDEs, etc.).
  This can be mitigated if your shool provides some way
  to provide students with a consistent environment (e.g., shared server,
  computer labs, or school provided laptops).
* Creates shared dependencies between applications which may make installing
  and upgrading software more challenging on the same system.

### 2.2. Docker Environment

We provide pre-built Docker containers installed with PLCC and its dependencies.
To use them locally, one needs Docker Desktop installed and running on their
local machine. To gain access to PLCC commands, one can either start a
shell inside a PLCC container or can issue a command to run inside a PLCC
container; both can operate on code on the local file system by mounting it
into the PLCC container. Either way, the PLCC container can be downloaded,
installed, and ran using a single docker command.

Advantages

* Avoids or reduces the disadvantages of installing into a native environment.
* The PLCC container has been tested.
* Updating to a new version of the PLCC container, or rolling back to an older
  release is easy and will not break other applications running on your system.
* If Docker Desktop is installed in a computer lab, you can upgrade or
  rollback to different versions of the PLCC container without needing to
  get permission or help from your IT division.

Disadvantages

* Docker Desktop must be installed and running on each students machine.
  Although it has become easier to install, there are still some gotchas
  if a student has an older machine.
* Docker Desktop requires a significant amount of memory
  (4GB RAM minimum; 8GB RAM more reasonably).
* Some familiarity with Docker may be helpful from time to time.
* The PLCC container is preinstalled with Java and Python, so you don't
  get to choose which version you want. You could build a custom Docker
  image with the versions you want, but this would require more advanced
  Docker knowledge and skills.

### 2.3. GitPod Workspace

GitPod provides temporary workspaces for repositories hosted on GitLab,
GitHub, or Bitbucket. If you are familiar with GitHub's CodeSpaces, GitPod
is similar but works with multiple repository hosting services and IDEs.
When one starts a workspace for a repository, they get an isolated development
environment pre-installed with the development tools necessary for working
on that project. Once can easily configure a repository to open a GitPod
workspace with PLCC and its dependencies pre-installed and ready for use.
All of these services are accessed through the Web, so there are no
software dependencies other than a Web-browser. However, individuals will
need a GitPod account, which provides 50 hours per month for free with
an associated LinkedIn account, and an account on the repository hosting
service (e.g., GitLab, GitHub, or Bitbucket) where the project resides.
If you and your students have a little familiarity with Git and one of
these hosting services, then this is likely the best option for you and
your students.

Advantages

* Only requires a Web-browser installed on each persons machine. So no
  one has to install anything on any machine!
* Configuring a repository for PLCC in GitPod is easy. No really, it is.
  See the installation section for GitPod below.
* Starting and using PLCC in a workspace for a project so configured is
  even easier.
* Each person works within an identical environment, which makes
  it much easier for instructors to support their students.
* Git and repository hosting services like GitLab, GitHub, and Bitbucket
  have become standard software development tools; so it's probably worth
  having students interact with them regularly.
* CodeSpaces and GitPod are fast becoming standard tools themselves.

Disadvantages

* Each person needs an account on the repository hosting service
  (GitLab, GitPod, or Bitbucket) that will be used and on GitPod.
* The instructor needs a good working knowledge of and skill with
  the repository hosting service and Git.
* Students do need a minimal understanding of and skill with
  the repository hosting service and Git.

The remaining sections will describe how to install and use PLCC in
each of these environments.

## 3. Install PLCC natively (Linux, Mac, or Windows)

In any order, you need to install PLCC's dependencies and PLCC itself.
Each are described below.

### 3.1. Install PLCC's dependencies

Installing PLCC requires that you also install a Java JDK
and Python, and know how to define and update environment
variables. 

PLCC requires the following to be installed and
available in your shell's path.

* Java JDK >= 11
* Python >= 3.5.10 ([Python](https://python.org/))

Installing a Java JDK has become complicated because there
are many different distributes with different licenses and support windows.
Consider installing [OpenJDK](https://openjdk.java.net/).

### 3.2. Install PLCC itself using the installer (Bash only)

If you are installing PLCC into a Bash environment, you can use the
installer (requires Git and Curl):

```bash
/bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)"
```

After following the instructions printed by the last command,
test your installation
(see "Test your PLCC installation" at the end of this document.).

If the above doesn't work for you, try following the manual installation
instructions next.

### 3.3. Install PLCC itself manually (Windows, Linux, or Mac)

If you are installing PLCC into another environment or the installer did not
work for you, you can install PLCC manually.

First, download a copy of PLCC. You can do this in two different ways:

* Use git to clone https://github.com/ourPLCC/plcc into its new home.
    ```bash
    git clone https://github.com/ourPLCC/plcc.git
    ```
* Download a zip of the desired version of PLCC from the
  [PLCC Releases page](https://github.com/ourPLCC/plcc/releases),
  and extract it into its new home on your computer.

Next, update your environment variables as follows:

1. Identify the PLCC's `src` directory within the directory (or subdirectories)
  created when you extracted the zip.
2. Define a new environment variable named `LIBPLCC` whose value is the
  full path to PLCC's `src` directory.
3. Add the full path to PLCC's `src` directory to beginning of the
  `PATH` environment variable.

Test your installation
(see "Test your PLCC installation" at the end of this document.).

## 4. Install and use in Docker

A Docker container is a lightweight virtual machine.
Using Docker Desktop, you can download, install,
and run a container in a single command.

Install and run
[Docker Desktop](https://www.docker.com/products/docker-desktop/).

With Docker Desktop running, the following mounts the
current working directory
into /workdir inside the container and starts an
interactive shell inside the container that has
access to all of the PLCC commands as well as
Java and Python. Any changes made to the files in
/workdir also change the files in the current
directory.

```bash
docker run --rm -it -v "${PWD}:/workdir" ghcr.io/ourplcc/plcc:latest
```

You can also run a single PLCC command on the code in your
current directory by appending the command and its
arguments to the same Docker command.

```bash
docker run --rm -it -v "${PWD}:/workdir" ghcr.io/ourplcc/plcc:latest PLCC_COMMANDS_HERE
```

To simplify, you could create a wrapper script or
function to hide all the extra docker stuff.
For example, here is a Bash function that does this.

```bash
# A Bash function
plcc-container () {
  docker run --rm -it -v "${PWD}:/workdir" ghcr.io/ourplcc/plcc:latest "$@"
}
```

Now you can start a shell inside the container like this.

```bash
plcc-container
```

Or run a command inside the container like this.

```bash
plcc-container plcc --version
```

Test your installation
(see "Test your PLCC installation" at the end of this document.).

## 5. Install and use in GitPod

GitPod provides workspaces (temporary development environments)
associated with a git repository on GitLab, GitHub, or Bitbucket.
This section describes how to configure a repository so that
PLCC is automatically installed into workspaces created for that
repository.

To configure your repository to install PLCC when opened in GitPod,
add or update `.gitpod.yml` in the root of a repository
in GitLab/GitHub/Bitbucket repository with the following:

```yaml
image: gitpod/workspace-full:latest

tasks:
  - name: Install PLCC
    command: |
        /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)" >> ~/.bashrc
        # Uncomment to checkout install specific version
        # git -C "$HOME/.local/plcc/" checkout v4.0.1
        exec bash
```

Open a new GitPod workspace for this repository and test your installation
(see "Test your PLCC installation" at the end of this document.).

## 6. Test your PLCC installation

Run the following commands in a new shell, terminal, or command-prompt
in the environment in which you installed PLCC.

```bash
plcc --version
java --version
javac --version
python3 --version
```

If all the commands produce version numbers, and the versions of java and
javac are the same, then you have successfully installed PLCC and are ready
to [learn to use PLCC](Use.md).
