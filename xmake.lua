set_project("cpp-quick-starter")
set_version("0.1.0")

set_languages("cxx20")
add_rules("mode.debug", "mode.release")

option("build_tests")
  set_default(true)
  set_showmenu(true)
  set_description("Build unit/integration tests")
option_end()

option("build_benchmarks")
  set_default(false)
  set_showmenu(true)
  set_description("Build benchmarks")
option_end()

option("build_examples")
  set_default(true)
  set_showmenu(true)
  set_description("Build examples")
option_end()

target("cpp_quick_starter")
  set_kind("static")
  add_headerfiles("include/(project_name/**.hpp)")
  add_files("src/core/**.cpp", "src/utils/**.cpp")
  add_includedirs("include", {public = true})
  if is_mode("debug") then
    add_defines("CPP_QUICK_STARTER_DEBUG", {public = true})
  end

  if is_plat("windows") then
    add_cxflags("/W4")
  else
    add_cxflags("-Wall", "-Wextra", "-Wpedantic")
  end

target_end()

target("cpp_quick_starter_app")
  set_kind("binary")
  add_files("src/main.cpp")
  add_deps("cpp_quick_starter")

target_end()

if has_config("build_examples") then
  target("example_01")
    set_kind("binary")
    add_files("examples/example_01.cpp")
    add_deps("cpp_quick_starter")

  target_end()
end

if has_config("build_tests") then
  add_requires("gtest")

  target("unit_tests")
    set_kind("binary")
    add_files("tests/unit/**.cpp")
    add_deps("cpp_quick_starter")
    add_packages("gtest")

  target_end()

  target("integration_tests")
    set_kind("binary")
    add_files("tests/integration/**.cpp")
    add_deps("cpp_quick_starter")
    add_packages("gtest")

  target_end()
end

if has_config("build_benchmarks") then
  add_requires("benchmark")

  target("benchmarks")
    set_kind("binary")
    add_files("benchmarks/**.cpp")
    add_deps("cpp_quick_starter")
    add_packages("benchmark")

  target_end()
end

task("docs")
  set_menu {
    usage = "xmake docs",
    description = "Build MkDocs documentation",
    options = {
      {"o", "outputdir", "kv", "site", "build/mkdocs"}
    }
  }
  on_run(function ()
    import("core.base.option")
    import("lib.detect.find_tool")
    local uv = find_tool("uv")
    local mkdocs = find_tool("mkdocs")
    local cmd = nil
    local argv = {}
    if uv then
      cmd = uv.program
      argv = {"run", "mkdocs"}
    elseif mkdocs then
      cmd = mkdocs.program
    else
      local python = find_tool("python") or find_tool("python3")
      if python then
        cmd = python.program
        argv = {"-m", "mkdocs"}
      end
    end
    if not cmd then
      raise("mkdocs not found. Install via: pip install mkdocs")
    end
    local outputdir = option.get("outputdir") or "build/mkdocs"
    table.join2(argv, {"build", "-f", "mkdocs.yml", "-d", outputdir})
    os.execv(cmd, argv)
  end)

task("docs-serve")
  set_menu {
    usage = "xmake docs-serve",
    description = "Serve MkDocs documentation locally",
    options = {}
  }
  on_run(function ()
    import("core.base.option")
    import("lib.detect.find_tool")
    local uv = find_tool("uv")
    local mkdocs = find_tool("mkdocs")
    local cmd = nil
    local argv = {}
    if uv then
      cmd = uv.program
      argv = {"run", "mkdocs"}
    elseif mkdocs then
      cmd = mkdocs.program
    else
      local python = find_tool("python") or find_tool("python3")
      if python then
        cmd = python.program
        argv = {"-m", "mkdocs"}
      end
    end
    if not cmd then
      raise("mkdocs not found. Install via: pip install mkdocs")
    end
    table.join2(argv, {"serve", "-f", "mkdocs.yml"})
    os.execv(cmd, argv)
  end)

-- ============================================================================
-- CLI Script Integration Tasks
-- ============================================================================

-- Helper function to find Python and run CLI (must be called from on_run context)
function run_cqs(args)
  import("lib.detect.find_tool")
  local python = find_tool("python3") or find_tool("python")
  if not python then
    raise("Python not found. Please install Python 3.")
  end
  local script = path.join(os.scriptdir(), "scripts", "cqs.py")
  local argv = {script}
  table.join2(argv, args)
  os.execv(python.program, argv)
end

-- Helper function to run shell script (must be called from on_run context)
function run_script(unix_script, win_script, args)
  args = args or {}
  if is_plat("windows") then
    local script = path.join(os.scriptdir(), "scripts", win_script)
    os.execv("powershell", {"-ExecutionPolicy", "Bypass", "-File", script, table.unpack(args)})
  else
    local script = path.join(os.scriptdir(), "scripts", unix_script)
    os.execv("bash", {script, table.unpack(args)})
  end
end

-- Format code
task("format")
  set_menu {
    usage = "xmake format",
    description = "Format all source files with clang-format",
    options = {
      {"c", "check", "k", "Check only, don't modify files"}
    }
  }
  on_run(function ()
    import("core.base.option")
    local args = {}
    if option.get("check") then
      table.insert(args, "--check")
    end
    run_script("format.sh", "format.ps1", args)
  end)

-- Clean all
task("clean-all")
  set_menu {
    usage = "xmake clean-all",
    description = "Clean all build artifacts",
    options = {
      {"a", "all", "k", "Remove IDE caches too"}
    }
  }
  on_run(function ()
    import("core.base.option")
    local args = {}
    if option.get("all") then
      table.insert(args, "--all")
    end
    run_script("clean.sh", "clean.ps1", args)
  end)

-- Doctor - check environment
task("doctor")
  set_menu {
    usage = "xmake doctor",
    description = "Check development environment",
    options = {}
  }
  on_run(function ()
    import("lib.detect.find_tool")
    local python = find_tool("python3") or find_tool("python")
    if not python then
      raise("Python not found. Please install Python 3.")
    end
    local script = path.join(os.scriptdir(), "scripts", "cqs.py")
    os.execv(python.program, {script, "doctor"})
  end)

-- Info - show project info
task("info")
  set_menu {
    usage = "xmake info",
    description = "Show project information",
    options = {}
  }
  on_run(function ()
    import("lib.detect.find_tool")
    local python = find_tool("python3") or find_tool("python")
    if not python then
      raise("Python not found. Please install Python 3.")
    end
    local script = path.join(os.scriptdir(), "scripts", "cqs.py")
    os.execv(python.program, {script, "info"})
  end)

-- Init - interactive project initialization
task("init")
  set_menu {
    usage = "xmake init",
    description = "Initialize project interactively",
    options = {}
  }
  on_run(function ()
    import("lib.detect.find_tool")
    local python = find_tool("python3") or find_tool("python")
    if not python then
      raise("Python not found. Please install Python 3.")
    end
    local script = path.join(os.scriptdir(), "scripts", "cqs.py")
    os.execv(python.program, {script, "init"})
  end)

-- Add module
task("add-module")
  set_menu {
    usage = "xmake add-module",
    description = "Add a new module (interactive)",
    options = {}
  }
  on_run(function ()
    import("lib.detect.find_tool")
    local python = find_tool("python3") or find_tool("python")
    if not python then
      raise("Python not found. Please install Python 3.")
    end
    local script = path.join(os.scriptdir(), "scripts", "cqs.py")
    os.execv(python.program, {script, "add", "module"})
  end)

-- Add dependency
task("add-dep")
  set_menu {
    usage = "xmake add-dep",
    description = "Add a package dependency (interactive)",
    options = {}
  }
  on_run(function ()
    import("lib.detect.find_tool")
    local python = find_tool("python3") or find_tool("python")
    if not python then
      raise("Python not found. Please install Python 3.")
    end
    local script = path.join(os.scriptdir(), "scripts", "cqs.py")
    os.execv(python.program, {script, "add", "dep"})
  end)

-- CLI help
task("cli")
  set_menu {
    usage = "xmake cli [command]",
    description = "Run CLI scaffolding tool",
    options = {
      {nil, "command", "v", "CLI command to run", "help"}
    }
  }
  on_run(function ()
    import("core.base.option")
    import("lib.detect.find_tool")
    local cmd = option.get("command") or "help"
    local python = find_tool("python3") or find_tool("python")
    if not python then
      raise("Python not found. Please install Python 3.")
    end
    local script = path.join(os.scriptdir(), "scripts", "cqs.py")
    os.execv(python.program, {script, cmd})
  end)

-- Setup - check tools
task("setup")
  set_menu {
    usage = "xmake setup",
    description = "Check development environment setup",
    options = {
      {"d", "detail", "k", "Show detailed version info"}
    }
  }
  on_run(function ()
    import("core.base.option")
    local args = {}
    if option.get("detail") then
      table.insert(args, "-Verbose")
    end
    local script = path.join(os.scriptdir(), "scripts", "setup.ps1")
    if is_host("windows") then
      os.execv("powershell", {"-ExecutionPolicy", "Bypass", "-File", script, table.unpack(args)})
    else
      script = path.join(os.scriptdir(), "scripts", "setup.sh")
      os.execv("bash", {script, table.unpack(args)})
    end
  end)

-- Test with options
task("test")
  set_menu {
    usage = "xmake test",
    description = "Run tests",
    options = {
      {"d", "detail", "k", "Verbose output"},
      {"f", "filter", "kv", "Test filter pattern"}
    }
  }
  on_run(function ()
    import("core.base.option")
    local args = {}
    if option.get("detail") then
      table.insert(args, "-Verbose")
    end
    if option.get("filter") then
      table.insert(args, "-Filter")
      table.insert(args, option.get("filter"))
    end
    local script = path.join(os.scriptdir(), "scripts", "test.ps1")
    if is_host("windows") then
      os.execv("powershell", {"-ExecutionPolicy", "Bypass", "-File", script, table.unpack(args)})
    else
      script = path.join(os.scriptdir(), "scripts", "test.sh")
      os.execv("bash", {script, table.unpack(args)})
    end
  end)

-- Print available tasks on load
task("tasks")
  set_menu {
    usage = "xmake tasks",
    description = "List all available custom tasks",
    options = {}
  }
  on_run(function ()
    print([[
Available custom tasks:
  Build & Test:
    xmake test              - Run tests
    xmake format            - Format code
    xmake format -c         - Check formatting
    xmake clean-all         - Clean all artifacts

  Documentation:
    xmake docs              - Build documentation
    xmake docs-serve        - Serve documentation locally

  CLI Scaffolding:
    xmake init              - Initialize project (interactive)
    xmake add-module        - Add a new module
    xmake add-dep           - Add a dependency
    xmake info              - Show project information
    xmake doctor            - Check environment
    xmake setup             - Check development setup
    xmake cli [cmd]         - Run CLI command

  Help:
    xmake tasks             - Show this list
]])
  end)
