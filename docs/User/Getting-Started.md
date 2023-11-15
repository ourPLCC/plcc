There are two options for using PLCC. Each has its advantages and disadvantages.

* [Native PLCC Installation](Native-PLCC-Installation.md)
    * Advantages
        * Choice of what version of dependencies (Python, Java, and shell) to use.
    * Disadvantages
        * Must properly install and configure dependencies and PLCC.
        * Dependencies are shared with other software on your system, which could lead to maintenance challenges in the future.
* [PLCC-in-Docker (Docker Container)](PLCC-in-Docker.md)
    * Advantages
        * Docker is the only dependency you need to install.
        * PLCC container, preinstalled with dependencies, is downloaded, installed, and ran in a single command.
        * PLCC's dependencies are not shared with other software on your system, so future maintenance is easier.
    * Disadvantages
        * On a non-linux platform, Docker will require a fair amount of resources to run (4-8 GB memory).
        * To control versions of dependencies (Python, Java, and Bash), you'd have to create a custom Docker container.
