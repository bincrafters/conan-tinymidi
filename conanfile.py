# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import SystemPackageTool
import os


class TinyMidiConan(ConanFile):
    name = "tinymidi"
    version = "20130325"
    description = "a small C library for doing MIDI on GNU/Linux"
    topics = ("conan", "tinymidi", "MIDI")
    url = "https://github.com/bincrafters/conan-tinymidi"
    homepage = "https://github.com/krgn/tinymidi"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "LGPL-3.0-only"
    exports = ["LICENSE.md"]
    settings = {"os": ["Linux"], "arch": None, "compiler": None, "build_type": None}
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx

    def system_requirements(self):
        if tools.os_info.with_apt:
            installer = SystemPackageTool()
            installer.install("libtool-bin")

    def source(self):
        revision = "3162cf8faff04e26a8daa846618b90326f71b9d5"
        source_url = "https://github.com/krgn/tinymidi/archive/%s.zip" % revision
        tools.get(source_url, sha256="a3ffcbc463559c6db3cfe40510a9859502d51f4cf8033966073a1a58224d3476")
        extracted_dir = self.name + "-" + revision
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            tools.replace_in_file("Makefile",
                                  "INSTALL_PREFIX=/usr",
                                  "INSTALL_PREFIX=%s" % self.package_folder)
            tools.replace_in_file("Makefile", "COMPILE_FLAGS = ", "COMPILE_FLAGS = $(CFLAGS) ")
            tools.replace_in_file("Makefile", "LINKING_FLAGS = ", "LINKING_FLAGS = $(CFLAGS) ")
            tools.mkdir(os.path.join(self.package_folder, 'include'))
            tools.mkdir(os.path.join(self.package_folder, 'lib'))
            env_build = AutoToolsBuildEnvironment(self)
            env_build.make()
            env_build.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = ["tinymidi"]
