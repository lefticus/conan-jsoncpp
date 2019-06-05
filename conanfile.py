from conans import ConanFile, CMake, tools
import os, shutil


class JsoncppConan(ConanFile):
    name        = "jsoncpp"
    version     = "1.8.4"
    description = "A C++ library for interacting with JSON."
    url         = "https://github.com/theirix/conan-jsoncpp"
    license     = "MIT"
    homepage    = "https://github.com/open-source-parsers/jsoncpp"
    author      = "theirix <theirix@gmail.com>"
    settings    = "os", "compiler", "arch", "build_type"

    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators  = "cmake", "txt"

    # Workaround for long cmake binary path
    # short_paths = True

    options = {
        "shared"              : [True, False],
        "fPIC"             : [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": False
    }

    _source_subfolder = "source_subfolder"

    def configure(self):
        if self.options.shared:
            self.options.use_pic = True

    def source(self):
        checksum = "c49deac9e0933bcb7044f08516861a2d560988540b23de2ac1ad443b219afdb6"
        tools.get("https://github.com/open-source-parsers/jsoncpp/archive/%s.tar.gz" % self.version, sha256=checksum)
        os.rename("jsoncpp-%s" % self.version, self._source_subfolder)
        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"),
                  os.path.join(self._source_subfolder, "CMakeListsOriginal.txt"))
        shutil.copy("CMakeLists.txt",
                    os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def build(self):
        if self.settings.compiler == "Visual Studio" and self.settings.compiler.version == "11":
            tools.replace_in_file(os.path.join(self._source_subfolder, "include", "json", "value.h"),
                                  "explicit operator bool()",
                                  "operator bool()")
        cmake = CMake(self)

        cmake.definitions['JSONCPP_WITH_CMAKE_PACKAGE'] = True
        cmake.definitions['JSONCPP_WITH_TESTS'] = False
        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared
        cmake.definitions['BUILD_STATIC_LIBS'] = not self.options.shared

        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("license*", src=self._source_subfolder, dst="licenses", ignore_case=True, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['jsoncpp']
