project(GrpcReusePackage)
cmake_minimum_required(VERSION 3.5.1)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(Protobuf_LIBRARY ${CONAN_PROTOBUF_ROOT})
find_package(Protobuf)

get_filename_component(hw_proto "./helloworld.proto" ABSOLUTE)
get_filename_component(hw_proto_path "${hw_proto}" PATH)

# Generated sources
protobuf_generate_cpp(hw_proto_srcs hw_proto_hdrs "${hw_proto}")
set(hw_grpc_srcs "${CMAKE_CURRENT_BINARY_DIR}/helloworld.grpc.pb.cc")
set(hw_grpc_hdrs "${CMAKE_CURRENT_BINARY_DIR}/helloworld.grpc.pb.h")
add_custom_command(
      OUTPUT "${hw_grpc_srcs}" "${hw_grpc_hdrs}"
      COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
      ARGS --grpc_out "${CMAKE_CURRENT_BINARY_DIR}" -I ${hw_proto_path}
        --plugin=protoc-gen-grpc="${CONAN_BIN_DIRS_GRPC}/grpc_cpp_plugin"
        "${hw_proto}"
      DEPENDS "${hw_proto}")

# Generated include directory
include_directories("${CMAKE_CURRENT_BINARY_DIR}")

add_executable(greeter_combined greeter_combined.cc ${hw_proto_srcs} ${hw_grpc_srcs})

if(NOT APPLE AND NOT WIN32)
  set(EXTRA_LINK_FLAGS "-pthread")
endif()

target_link_libraries(greeter_combined PRIVATE
    -L${CONAN_LIB_DIRS_GRPC} grpc++_unsecure
    -L${CONAN_LIB_DIRS_PROTOBUF} ${CONAN_LIBS_PROTOBUF}
    -L${CONAN_LIB_DIRS_ZLIB} ${CONAN_LIBS_ZLIB}
    ${EXTRA_LINK_FLAGS})
