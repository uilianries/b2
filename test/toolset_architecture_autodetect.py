#!/usr/bin/env python3
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or copy at
# https://www.bfgroup.xyz/b2/LICENSE.txt)

# Test for autodetecting <architecture> from the compiler's own
# `-dumpmachine` triple when architecture is not given explicitly, covering
# the gcc, clang-linux and clang-darwin toolsets.

import BoostBuild
import sys
import textwrap

MOCK_COMPILER_TEMPLATE = '''#!/usr/bin/env python3
import sys

args = sys.argv[1:]

if args == ["-dumpmachine"]:
    print("@TRIPLE@")
    sys.exit(0)

if args == ["-print-prog-name=ar"]:
    print("ar")
    sys.exit(0)

if "-c" in args and "-o" in args:
    if "-DARCH_AUTODETECTED_OK" not in args:
        sys.exit(1)
    with open(args[args.index("-o") + 1], "w") as f:
        f.write("mock object\\n")
    sys.exit(0)

sys.exit(1)
'''


def test_architecture_gcc_autodetect():
    t = BoostBuild.Tester(pass_toolset=0)

    t.write("fake-compiler.py", MOCK_COMPILER_TEMPLATE.replace("@TRIPLE@", "x86_64-linux-gnu"))
    t.write("project-config.jam", textwrap.dedent('''
        import os ;
        path-constant HERE : . ;
        local PYTHON = [ os.environ PYTHON_CMD ] ;
        using gcc : autodetect : $(PYTHON) $(HERE)/fake-compiler.py ;
        '''))
    t.write("Jamroot.jam", textwrap.dedent('''
        obj test : test.cpp :
        <architecture>x86:<define>ARCH_AUTODETECTED_OK ;
        '''))
    t.write("test.cpp", "int f() { return 0; }")

    t.run_build_system([f"-sPYTHON_CMD={sys.executable}", "toolset=gcc-autodetect", "test"])
    t.cleanup()

def test_architecture_clang_linux_autodetect():
    t = BoostBuild.Tester(pass_toolset=0)

    t.write("fake-compiler.py", MOCK_COMPILER_TEMPLATE.replace("@TRIPLE@", "aarch64-linux-gnu"))
    t.write("project-config.jam", textwrap.dedent('''
        import os ;
        path-constant HERE : . ;
        local PYTHON = [ os.environ PYTHON_CMD ] ;
        using clang-linux : autodetect : $(PYTHON) $(HERE)/fake-compiler.py ;
        '''))
    t.write("Jamroot.jam", textwrap.dedent('''
        obj test : test.cpp :
        <architecture>arm:<define>ARCH_AUTODETECTED_OK ;
        '''))
    t.write("test.cpp", "int f() { return 0; }")

    t.run_build_system([f"-sPYTHON_CMD={sys.executable}", "toolset=clang-linux-autodetect", "test"])
    t.cleanup()

def test_architecture_clang_linux_autodetect_power():
    t = BoostBuild.Tester(pass_toolset=0)

    t.write("fake-compiler.py", MOCK_COMPILER_TEMPLATE.replace("@TRIPLE@", "powerpc64le-linux-gnu"))
    t.write("project-config.jam", textwrap.dedent('''
        import os ;
        path-constant HERE : . ;
        local PYTHON = [ os.environ PYTHON_CMD ] ;
        using clang-linux : autodetect : $(PYTHON) $(HERE)/fake-compiler.py ;
        '''))
    t.write("Jamroot.jam", textwrap.dedent('''
        obj test : test.cpp :
        <architecture>power:<define>ARCH_AUTODETECTED_OK ;
        '''))
    t.write("test.cpp", "int f() { return 0; }")

    t.run_build_system([f"-sPYTHON_CMD={sys.executable}", "toolset=clang-linux-autodetect", "test"])
    t.cleanup()

def test_architecture_clang_darwin_autodetect():
    t = BoostBuild.Tester(pass_toolset=0)

    t.write("fake-compiler.py", MOCK_COMPILER_TEMPLATE.replace("@TRIPLE@", "arm64-apple-darwin23"))
    t.write("project-config.jam", textwrap.dedent('''
        import os ;
        path-constant HERE : . ;
        local PYTHON = [ os.environ PYTHON_CMD ] ;
        using clang-darwin : autodetect : $(PYTHON) $(HERE)/fake-compiler.py ;
        '''))
    t.write("Jamroot.jam", textwrap.dedent('''
        obj test : test.cpp :
        <architecture>arm:<define>ARCH_AUTODETECTED_OK ;
        '''))
    t.write("test.cpp", "int f() { return 0; }")

    t.run_build_system([f"-sPYTHON_CMD={sys.executable}", "toolset=clang-darwin-autodetect", "test"])
    t.cleanup()


def test_architecture_clang_darwin_autodetect_linux():
    t = BoostBuild.Tester(pass_toolset=0)

    t.write("fake-compiler.py", MOCK_COMPILER_TEMPLATE.replace("@TRIPLE@", "riscv64-unknown-linux-gnu"))
    t.write("project-config.jam", textwrap.dedent('''
        import os ;
        path-constant HERE : . ;
        local PYTHON = [ os.environ PYTHON_CMD ] ;
        using clang-darwin : autodetect : $(PYTHON) $(HERE)/fake-compiler.py ;
        '''))
    t.write("Jamroot.jam", textwrap.dedent('''
        obj test : test.cpp :
        <architecture>riscv:<define>ARCH_AUTODETECTED_OK ;
        '''))
    t.write("test.cpp", "int f() { return 0; }")

    t.run_build_system([f"-sPYTHON_CMD={sys.executable}", "toolset=clang-darwin-autodetect", "test"])
    t.cleanup()


test_architecture_gcc_autodetect()
test_architecture_clang_linux_autodetect()
test_architecture_clang_linux_autodetect_power()
test_architecture_clang_darwin_autodetect()
test_architecture_clang_darwin_autodetect_linux()
