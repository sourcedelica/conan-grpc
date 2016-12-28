from conans import ConanFile, CMake


class GrpcReuseConan(ConanFile):
    version = '1.0.1'
    username = 'sourcedelica'                            # FIXME
    channel = 'testing'                                  # FIXME
    requires = "grpc/%s@sourcedelica/testing" % version, \
               "Protobuf/3.0.2@sourcedelica/testing"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dylib", "bin", src="lib")
        self.copy("*.dll",   "bin", src="bin")

    def test(self):
        self.run("bin/greeter_combined")
