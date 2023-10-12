#!/usr/bin/env bash
# Idempotent setup script which installs glfw (and any other ccircle dependencies).
# TODO: port this file to asdf...

set -eo pipefail
# Function to display an error message and exit
function error_message {
    printf "\nFATAL ERROR: Something went wrong. Script exiting.\n"
    exit 1
}
# Set up a trap to display the error message upon script exit
trap 'if [ $? -ne 0 ]; then display_error; fi' EXIT

################## IDEMPOTENT HELPER FUNCTIONS #####################
# Install brew.
function ensure_brew() {
    command -v brew >/dev/null 2>&1 || { echo >&2 "Installing Homebrew Now..."; \
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; }

    echo >&2 "Homebrew install confirmed."
}

# Install GLFW (glfw3) shared library binary view Homebrew.
function ensure_glfw_shared_library() {
    brew list glfw >/dev/null 2>&1 || { echo >&2 "Installing glfw shared library..."; \
    brew install glfw; }

    # After glfw is installed we need to set an environment variable so it is picked up by pyglfw.
    # First, ensure the dylib is in the canonical install location.
    local required_dylib_name='libglfw3.dylib'
    local required_dylib_base_path="/usr/local/Cellar/glfw/3.3.8/lib"
    local homebrew_installed_dylib_file=$(brew list glfw | grep libglfw.3.3.dylib)
    [[ -f ${homebrew_installed_dylib_file} ]] || { echo >&2 "Was expecting glfw dylib at location $homebrew_installed_dylib_file"; \
    exit 1;}

     # Ensure the dylib path is as expected by pyGlfw.
    if [[ ! -f "$required_dylib_base_path/$required_dylib_name" ]]; then
        echo "Sudo / password required to create the directories for path $required_dylib_base_path"
        sudo mkdir -p "$required_dylib_base_path"
        local command="sudo ln -s $homebrew_installed_dylib_file $required_dylib_base_path/$required_dylib_name"
        echo >&2 "Creating a symlink for expected pyGlfw filename: $command"
        eval "${command}"
    fi

    echo >&2 "glfw shared library install confirmed."
}

## Install glfw: https://pypi.org/project/glfw/.
#function ensure_pyglfw() {
#    { pip freeze | grep glfw >/dev/null 2>&1; } || { echo >&2 "Installing python bindings for glfw..."; \
#    pip install glfw; }
#
#    echo >&2 "glfw (python bindings) install confirmed."
#}
#
## Install pyOpenGL.
#function ensure_pyopengl() {
#    { pip freeze | grep PyOpenGL >/dev/null 2>&1; } || { echo >&2 "Installing PyOpenGL..."; \
#    pip install PyOpenGL; }
#
#    echo >&2 "PyOpenGL install confirmed."
#}
################# MAIN #####################
ensure_brew # OSX Package manager.
ensure_glfw_shared_library # OS-specific shared library.
#ensure_pyglfw # Python bindings for glfw.
#ensure_pyopengl

echo -e >&2 "\n---Ccircle dependencies confirmed.---"