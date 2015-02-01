from cx_Freeze import setup, Executable

linux_target = Executable(
    script = "fng/app.py",
    targetName = "fng"
    )

setup(name = "fng",
      version = "0.1",
      description = "",
#      executables = [Executable("fng/app.py")] , )
      executables = [linux_target], )
