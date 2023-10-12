![](docs/screenshots/coding_circle.jpeg)
>Learn to code via interactive games!
<hr>


## Setup / Documentation
> Note: Setup has only been validated against arm64 OSX.

1. Ensure system has `asdf`.
   1. `brew install coreutils curl git asdf`
1. Ensure system has poetry (via asdf).
    1. `asdf ensure-versions`
1. Ensure poetry installs deps in a .venv directory.
   1. `poetry config virtualenvs.in-project true --local`
1. Install dependencies via `poetry`
   1. `poetry install`
1. Ensure the system has `glfw`. TODO(move this to poetry).
    1. `pip install glfw`
1. Validate your setup by running `02_cc_hello.py` in PyCharm or on the CLI via:
   1. ```
      PYTHONPATH=$PWD \
      poetry run python cc_student/hello_world/02_cc_hello.py
      ```

> TODO(Brendan): Move this info to the setup section of [the docs](https://mithridatize.github.io/ccircle/).

## Screenshots
### Scenario 1
![](docs/screenshots/scenario01_easy.png)
### Scenario 2
![](docs/screenshots/scenario02.png)


## Highlights
* No prior programming experience required.
* Learn to use a professional development toolchain.
* Almost everything is written in Python,
    so you can explore 'how does this work?' as much as you want.
* Learn the fundamentals of a breadth of computer science topics:
    * Object Oriented Programming (OOP)
    * 2D Game Development (Modern OpenGL 3.2+)
    * Multi-player Game Development: Client/Server (http & tcp)
    * TODO
        * Audio Synthesis
        * Data Structures
        * Databases
        * AI
        * Machine Learning
        * Security / Cryptography 
        * Various 3D Graphics topics:
            * Quaternions and matrix math
            * Ray-tracing
            * Bounding Boxes and Object collision
  

## TODO
- Hackathon stuff
  - [x] swap dependency mgmt to poetry
  - [x] upgrade dependencies to work on arm64
    - [x] upgrade deps minimally 
    - [x] confirm upgrade via 02_cc_hello.py
  - [x] upgrade from python 3.7?)
  - [x] MVP freight game UI -> scenario05
  - [ ] MVP freight game setup
  - [ ] game AI
  - [ ] compare game AI results to user's algo
  - [ ] toggle game AI
  - [ ] ...
- Pipenv
    - [ ] stop pinning versions (migrate to *)
    - [ ] clean up dependencies
- [ ] get [Trial tests](https://twisted.readthedocs.io/en/twisted-18.9.0/core/howto/trial.html) working
- [ ] Unit Tests (against stored image).
- [ ] pip distribute ccircle prep [here](https://setuptools.readthedocs.io/en/latest/setuptools.html#distributing-a-setuptools-based-project)
  - [ ] Ensure Windows Support once moved to ccircle as pip-distributed package. 
- Uncategorized 
    - [ ] Template /generate endpoint for cc_student instead of cloning repo (after split to pip distribute).
    - [ ] Documentation via GitBooks.
    - [ ] Pretend to be new, make youtube video of setup: 'Intro to Software Development'.
    - [ ] Walk through it with someone, take notes for improvement.
    - [ ] Slack community.
- [ ] All topics covered under Highlights.
  - [ ] Scenario 3: rush hour.
  - [ ] EDM DJ name generator (phonetics model -> kshmr is good)
  - [ ] Make [snowball fight](https://www.youtube.com/watch?v=x0z-qhnMuc0)! 
- Minor
  - [ ] Adapt things from [intro to python pdf](https://python.swaroopch.com/problem_solving.html)
  - [ ] Scenario or walkthrough like 
        [Writing a Program that Edits my Videos](https://www.youtube.com/watch?v=0ZeO0IQaJ-A)
