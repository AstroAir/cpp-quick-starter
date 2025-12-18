# Scripts.cmake - Integration of CLI scaffolding tools into CMake
#
# This module provides custom targets for common development tasks:
#   - format / format-check : Code formatting
#   - clean-all            : Clean build artifacts
#   - doctor               : Check development environment
#   - info                 : Show project information
#   - add-module           : Add a new module (interactive)
#   - add-dep              : Add a dependency (interactive)
#
# Usage in CMakeLists.txt:
#   include(Scripts)
#   add_script_targets()

find_package(Python3 COMPONENTS Interpreter QUIET)

# Find the scripts directory
set(CPP_QUICK_STARTER_SCRIPTS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/scripts")

# Helper function to create a script target
function(add_script_target TARGET_NAME SCRIPT_PATH)
    set(options INTERACTIVE)
    set(oneValueArgs DESCRIPTION WORKING_DIR)
    set(multiValueArgs ARGS)
    cmake_parse_arguments(SCRIPT "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    if(NOT SCRIPT_WORKING_DIR)
        set(SCRIPT_WORKING_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
    endif()

    if(NOT SCRIPT_DESCRIPTION)
        set(SCRIPT_DESCRIPTION "Run ${TARGET_NAME}")
    endif()

    if(Python3_FOUND)
        add_custom_target(${TARGET_NAME}
            COMMAND ${Python3_EXECUTABLE} "${SCRIPT_PATH}" ${SCRIPT_ARGS}
            WORKING_DIRECTORY "${SCRIPT_WORKING_DIR}"
            COMMENT "${SCRIPT_DESCRIPTION}"
            USES_TERMINAL
        )
    else()
        add_custom_target(${TARGET_NAME}
            COMMAND ${CMAKE_COMMAND} -E echo "Python3 not found. Cannot run ${TARGET_NAME}."
            COMMENT "Python3 required for ${TARGET_NAME}"
        )
    endif()
endfunction()

# Helper function to create a shell script target
function(add_shell_script_target TARGET_NAME)
    set(options)
    set(oneValueArgs DESCRIPTION WORKING_DIR UNIX_SCRIPT WIN_SCRIPT)
    set(multiValueArgs UNIX_ARGS WIN_ARGS)
    cmake_parse_arguments(SCRIPT "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    if(NOT SCRIPT_WORKING_DIR)
        set(SCRIPT_WORKING_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
    endif()

    if(NOT SCRIPT_DESCRIPTION)
        set(SCRIPT_DESCRIPTION "Run ${TARGET_NAME}")
    endif()

    if(WIN32)
        if(SCRIPT_WIN_SCRIPT)
            add_custom_target(${TARGET_NAME}
                COMMAND powershell -ExecutionPolicy Bypass -File "${SCRIPT_WIN_SCRIPT}" ${SCRIPT_WIN_ARGS}
                WORKING_DIRECTORY "${SCRIPT_WORKING_DIR}"
                COMMENT "${SCRIPT_DESCRIPTION}"
                USES_TERMINAL
            )
        endif()
    else()
        if(SCRIPT_UNIX_SCRIPT)
            add_custom_target(${TARGET_NAME}
                COMMAND bash "${SCRIPT_UNIX_SCRIPT}" ${SCRIPT_UNIX_ARGS}
                WORKING_DIRECTORY "${SCRIPT_WORKING_DIR}"
                COMMENT "${SCRIPT_DESCRIPTION}"
                USES_TERMINAL
            )
        endif()
    endif()
endfunction()

# Main function to add all script targets
function(add_script_targets)
    # === Code Formatting ===
    add_shell_script_target(format
        DESCRIPTION "Format all source files with clang-format"
        UNIX_SCRIPT "${CPP_QUICK_STARTER_SCRIPTS_DIR}/format.sh"
        WIN_SCRIPT "${CPP_QUICK_STARTER_SCRIPTS_DIR}/format.ps1"
    )

    add_shell_script_target(format-check
        DESCRIPTION "Check code formatting (CI mode)"
        UNIX_SCRIPT "${CPP_QUICK_STARTER_SCRIPTS_DIR}/format.sh"
        WIN_SCRIPT "${CPP_QUICK_STARTER_SCRIPTS_DIR}/format.ps1"
        UNIX_ARGS "--check"
        WIN_ARGS "-Check"
    )

    # === Clean ===
    add_shell_script_target(clean-all
        DESCRIPTION "Clean all build artifacts"
        UNIX_SCRIPT "${CPP_QUICK_STARTER_SCRIPTS_DIR}/clean.sh"
        WIN_SCRIPT "${CPP_QUICK_STARTER_SCRIPTS_DIR}/clean.ps1"
        UNIX_ARGS "--all"
        WIN_ARGS "-All"
    )

    # === CLI Tools (Python) ===
    if(Python3_FOUND)
        set(CQS_SCRIPT "${CPP_QUICK_STARTER_SCRIPTS_DIR}/cqs.py")

        # Doctor - check development environment
        add_script_target(doctor
            "${CQS_SCRIPT}"
            DESCRIPTION "Check development environment"
            ARGS "doctor"
        )

        # Info - show project information
        add_script_target(info
            "${CQS_SCRIPT}"
            DESCRIPTION "Show project information"
            ARGS "info"
        )

        # Add module (interactive)
        add_script_target(add-module
            "${CQS_SCRIPT}"
            DESCRIPTION "Add a new module (interactive)"
            ARGS "add" "module"
        )

        # Add dependency (interactive)
        add_script_target(add-dep
            "${CQS_SCRIPT}"
            DESCRIPTION "Add a dependency (interactive)"
            ARGS "add" "dep"
        )

        # Help
        add_script_target(cli-help
            "${CQS_SCRIPT}"
            DESCRIPTION "Show CLI help"
            ARGS "help"
        )
    endif()

    # === Convenience Aliases ===
    # Create 'lint' as alias for format-check
    if(TARGET format-check)
        add_custom_target(lint DEPENDS format-check)
    endif()

    # === Print available targets ===
    message(STATUS "Script targets available:")
    message(STATUS "  cmake --build build --target format       - Format code")
    message(STATUS "  cmake --build build --target format-check - Check formatting")
    message(STATUS "  cmake --build build --target clean-all    - Clean all artifacts")
    if(Python3_FOUND)
        message(STATUS "  cmake --build build --target doctor       - Check environment")
        message(STATUS "  cmake --build build --target info         - Project info")
        message(STATUS "  cmake --build build --target add-module   - Add new module")
        message(STATUS "  cmake --build build --target add-dep      - Add dependency")
    endif()
endfunction()

# Utility function to run tests with coverage
function(add_coverage_target)
    find_program(GCOVR_PROGRAM gcovr)
    find_program(LCOV_PROGRAM lcov)

    if(GCOVR_PROGRAM)
        add_custom_target(coverage
            COMMAND ${CMAKE_COMMAND} -E make_directory "${CMAKE_BINARY_DIR}/coverage"
            COMMAND ${GCOVR_PROGRAM}
                --root "${CMAKE_SOURCE_DIR}"
                --object-directory "${CMAKE_BINARY_DIR}"
                --html --html-details
                --output "${CMAKE_BINARY_DIR}/coverage/index.html"
            WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
            COMMENT "Generating coverage report with gcovr"
            DEPENDS unit_tests
        )
        message(STATUS "  cmake --build build --target coverage     - Generate coverage")
    elseif(LCOV_PROGRAM)
        add_custom_target(coverage
            COMMAND ${LCOV_PROGRAM} --capture --directory "${CMAKE_BINARY_DIR}" --output-file coverage.info
            COMMAND ${LCOV_PROGRAM} --remove coverage.info '/usr/*' --output-file coverage.info
            COMMAND genhtml coverage.info --output-directory "${CMAKE_BINARY_DIR}/coverage"
            WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
            COMMENT "Generating coverage report with lcov"
            DEPENDS unit_tests
        )
    endif()
endfunction()
