# import os
# from conan.tools.build import check_min_cppstd

from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMakeDeps, CMakeToolchain, cmake_layout, CMake


class Rocos(ConanFile):
    name = "rocos"
    version = "0.0.3"

    # description = "Rocos."
    # license = "GPL-3.0"
    homepage = "https://github.com/Robocup-ssl-China/rocos"
    topics = "Rocos"

    settings = "os", "compiler", "build_type", "arch"

    # 从项目库获取本包需要构建的 rocos 源代码
    def source(self):
        pass
        # git = Git(self)
        # git.clone(url="https://github.com/Robocup-ssl-China/rocos.git", target=".")
        # git.checkout("main")

    # 依赖库
    def requirements(self):
        self.requires("opengl/system")
        self.requires("eigen/3.4.0")
        self.requires("fmt/9.1.0")
        self.requires("protobuf/5.27.0")
        self.requires("ode/0.16.2")

        # 对特定环境添加对应的依赖库
        if self.settings.os == "Windows":
            self.requires("qt/[~5]")  # conan 的 qt 仅支持 Windows（还需测试）

    # 依赖库（构建依赖）
    def build_requirements(self):
        pass
        # self.requires("cmake/3.22.6")
        # 因为构建依赖库中没有预先编译好的二进制文件包需要 cmake ，所以 cmake 应该提前准备好
        # 在构建 rocos 中没有特别的版本需求，所以这里没有对 cmake 写进需求

    def layout(self):
        cmake_layout(self)

    # 生成依赖项所需
    def generate(self):
        cmake_deps = CMakeDeps(self)
        cmake_deps.generate()

        cmake_toolchain = CMakeToolchain(self)
        cmake_toolchain.generate()

    # def build(self):
    #     cmake = CMake(self)
    #     cmake.configure()
    #     cmake.build()
    #
    # =================== DO NOT USE ===================
    #     NOTE: 思路错误的部分，留着作为 self.run 的格式参考
    #
    #     cmake.configure(build_script_folder="lua")
    #     cmake.build()
    #     if self.settings.os != "Windows":
    #         self.run(f"rm {self.build_folder}/CMakeCache.txt")
    #     cmake.configure(build_script_folder="toluapp")
    #     cmake.build()
    #     if self.settings.os != "Windows":
    #         self.run(f"rm {self.build_folder}/CMakeCache.txt")
    #     cmake.configure(build_script_folder="protobuf")
    #     cmake.build()
    #     if self.settings.os != "Windows":
    #         self.run(f"rm {self.build_folder}/CMakeCache.txt")
    #     cmake.configure(build_script_folder="rocos")
    # =================== DO NOT USE ===================

    # def package(self):
    #     cmake = CMake(self)
    #     cmake.install()

    # def package_info(self):
    #     # 设置相关环境变量，供其他包使用
    #     self.cpp_info.libs = ["lua", "toluapp"]


"""=================== 目前的操作流程 ===================

sudo apt install python-pip3 git cmake
# 前者拿来装 conan，再者如果需要 clone 项目库到本地，后者从源代码 构建依赖库用

sudo apt install libgl-dev libgl1-mesa-dev pkg-config qtbase5-dev qtdeclarative5-dev libqt5serialport5-dev qml-module-qtquick* qml-module-qtgamepad libtolua++5.1-dev
# 缺少的话会在 install 阶段报错
# 暂时无法用 Conan 包代替的部分，主要为 gl、qt 和 tolua++ (& lua 5.1)

pip install conan # 部署 Conan

conan profile detect # 生成 Conan 配置

cd ~ && git clone https://github.com/Robocup-ssl-China/rocos.git && cd rocos

cp path/to/conanfile.py ~/rocos/conanfile.py

conan install . --build=missing # 安装依赖库，生成文件在 project_folder/build/Release/generators 下

cd ./build/Release/

source ./generators/conanbuild.sh # 进入提供的虚拟环境

# cmake>=3.23
cmake --preset conan-release
# cmake<3.23
cmake <path> -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=generators/conan_toolchain.cmake  -DCMAKE_POLICY_DEFAULT_CMP0091=NEW -DCMAKE_BUILD_TYPE=Release

cmake --build . # 构建成功后所有编译出来的内容在 project_folder/build/Release

source ./generators/deactivate_conanbuild.sh # 退出虚拟环境

project_folder/build/Release/ZBin/Client

"""
