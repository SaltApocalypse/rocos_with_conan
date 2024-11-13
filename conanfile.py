# import os
# from conan.tools.build import check_min_cppstd

from conan import ConanFile
from conan.tools.cmake import cmake_layout


class Rocos(ConanFile):
    name = "rocos"
    version = "0.0.3"

    # description = "Rocos."
    # license = "GPL-3.0"
    homepage = "https://github.com/Robocup-ssl-China/rocos"
    topics = "Rocos"

    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"

    # 依赖库
    def requirements(self):
        self.requires("opengl/system")
        self.requires("eigen/3.4.0")
        self.requires("fmt/9.1.0")
        self.requires("protobuf/5.27.0")
        self.requires("ode/0.16.2")

        # if self.settings.os == "Windows":
        #     self.requires("qt/[~5]")  # conan 的 qt 仅支持 Windows（还需测试）

    # 依赖库（构建依赖）
    def build_requirements(self):
        self.requires("cmake/[>=3.23]")

    def layout(self):
        cmake_layout(self)


"""=================== 目前的操作流程 ===================

sudo apt install python-pip3 git cmake
# 前者拿来装 conan，再者如果需要 clone 项目库到本地，后者从源代码 构建依赖库用

sudo apt install libgl-dev libgl1-mesa-dev pkg-config qtbase5-dev qtdeclarative5-dev libqt5serialport5-dev qml-module-qtquick* qml-module-qtgamepad libtolua++5.1-dev
# 暂时无法用 Conan 包代替的部分，主要为 gl、qt 和 tolua++ (& lua 5.1)

pip install conan # 部署 Conan

conan profile detect # 生成 Conan 配置

cd ~ && git clone https://github.com/Robocup-ssl-China/rocos.git && cd rocos

cp path/to/conanfile.py ~/rocos/conanfile.py

conan install . --output-folder=build --build=missing

source ./build/conanbuild.sh # 进入提供的虚拟环境

# cmake>=3.23
cmake --preset conan-release
# cmake<3.23
cmake <path> -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=generators/conan_toolchain.cmake  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW -DCMAKE_BUILD_TYPE=Release

cmake --build .

source ./build/deactivate_conanbuild.sh # 退出虚拟环境

======================================"""
