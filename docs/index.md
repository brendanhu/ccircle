* TOC
{:toc}

## Setup
> Step-by-step instructions--with screenshots--to get you running Ccircle effortlessly.

[Ccircle.Setup](environment_setup/index.md)

## Updating Ccircle
> How to get new instructor code.

[Ccircle.Update](environment_setup/git/pull_staff_changes/pullStaffChanges.md)


## Resources
> Hand-built reference PDF and exercises for students.

* [Python Quick Reference](Python_Quick_Reference.pdf)
* Labs:
  * [Python Lists, Functions and Objects](labs/lab03.md)
  * [Python Dictionaries](labs/lab04.md)


## Ccircle Codebase Explained
The following gives a brief summary of the `ccircle` directory structure as it concerns a student (you):
* [ccircle](https://github.com/brendanhu/ccircle/tree/master/cc):
    The base directory.
  * [cc](https://github.com/brendanhu/ccircle/tree/master/cc):
    The code for the cc python module. **You shouldn't modify anything in this directory.**
    * [setup](https://github.com/brendanhu/ccircle/tree/master/cc/setup):
        Install scripts that are referenced in the [setup](environment_setup/index.md).
  * [**cc_student**](https://github.com/brendanhu/ccircle/tree/master/cc_student):
    Contains all exercises (labs/scenarios/projects) you will work on.
    * [assets](https://github.com/brendanhu/ccircle/tree/master/cc_student/assets):
        Things like fonts and images you can use for various labs/projects.
    * [hello_world](https://github.com/brendanhu/ccircle/tree/master/cc_student/hello_world):
        Hello-world python files that demonstrate functionality or validate system setup.
    * [scenarioXX](https://github.com/brendanhu/ccircle/tree/master/cc_student/scenario01):
        All code for a scenario XX. The only file you will write code in is solution.py.
      * [skeleton](https://github.com/brendanhu/ccircle/tree/master/cc_student/scenario01/skeleton):
        Skeleton code given by the professor.
      * [**README.md**](https://github.com/brendanhu/ccircle/blob/master/cc_student/scenario01/README.md):
        A document detailing the scenario.
      * [scenarioXX.py](https://github.com/brendanhu/ccircle/blob/master/cc_student/scenario01/scenario01.py):
        The python file to run to test out your code / display the window.
      * [solution.py](https://github.com/brendanhu/ccircle/blob/master/cc_student/scenario01/solution.py):
        A file with an incomplete function for you to complete.
    * [incomplete](https://github.com/brendanhu/ccircle/tree/master/cc_student/incomplete):
        Incomplete exercises that I'm getting to. If you're snooping around and you see something
        interesting you want finished then send me an email; i am easily swayed by (even mild) enthusiasm.
  * [docs](https://github.com/brendanhu/ccircle/tree/master/docs):
    The raw versions of documents to be read for various labs/projects; they are presented in a prettier form via Github Pages.


## Git Walkthroughs
> If you want to save your work on the could, you can try using git!

* [Registering for GitHub](environment_setup/git/github_register/githubRegister.md)
* [Downloading Git](environment_setup/git/git_download/git_download.md)
* [Saving Code Online Using Git](environment_setup/git/git_push/saveToGit.md)
* [Pulling Saved Code From GitHub On a Different Computer](environment_setup/git/git_new_clone/gitNewClone.md)
