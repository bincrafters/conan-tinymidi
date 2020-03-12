from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import SystemPackageTool
from conans.errors import ConanInvalidConfiguration
import os


class TinyMidiConan(ConanFile):
    name = "tinymidi"
    description = "A small C library for doing MIDI on GNU/Linux"
    topics = ("conan", "tinymidi", "MIDI")
    url = "https://github.com/bincrafters/conan-tinymidi"
    homepage = "https://github.com/krgn/tinymidi"
    license = "LGPL-3.0-only"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    build_requires = "libtool/2.4.6"

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration("Only Linux is supported")

    def source(self):
        commit = os.path.splitext(os.path.basename(self.conan_data["sources"][self.version]["url"]))[0]
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + commit
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

    def package(self):
        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.install()
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        if self.options.shared:
            os.unlink(os.path.join(self.package_folder, "lib", "libtinymidi.a"))
        else:
            os.unlink(os.path.join(self.package_folder, "lib", "libtinymidi.so"))
            os.unlink(os.path.join(self.package_folder, "lib", "libtinymidi.so.1"))
            os.unlink(os.path.join(self.package_folder, "lib", "libtinymidi.so.1.0.0"))

    def package_info(self):
        self.cpp_info.libs = ["tinymidi"]
