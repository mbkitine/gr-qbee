INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_QBEE qbee)

FIND_PATH(
    QBEE_INCLUDE_DIRS
    NAMES qbee/api.h
    HINTS $ENV{QBEE_DIR}/include
        ${PC_QBEE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    QBEE_LIBRARIES
    NAMES gnuradio-qbee
    HINTS $ENV{QBEE_DIR}/lib
        ${PC_QBEE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(QBEE DEFAULT_MSG QBEE_LIBRARIES QBEE_INCLUDE_DIRS)
MARK_AS_ADVANCED(QBEE_LIBRARIES QBEE_INCLUDE_DIRS)

