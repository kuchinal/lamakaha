#
# Copyright (C) 2022  Autodesk, Inc. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

INCLUDE(cxx_defaults)

SET(_target
    "rvpkg"
)

LIST(APPEND _sources main.cpp utf8Main.cpp)

ADD_EXECUTABLE(
  ${_target}
  ${_sources}
)

FIND_PACKAGE(
  Qt5
  COMPONENTS Core
  REQUIRED
)

TARGET_INCLUDE_DIRECTORIES(
  ${_target}
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}
)

TARGET_LINK_LIBRARIES(
  ${_target}
  PRIVATE TwkApp
          TwkDeploy
          TwkExc
          TwkUtil
          stl_ext
          RvPackage
          arg
          stl_ext
          Qt5::Core
)

IF(RV_TARGET_DARWIN)
  TARGET_LINK_LIBRARIES(
    ${_target}
    PRIVATE DarwinBundle
  )
ELSE()
  TARGET_LINK_LIBRARIES(
    ${_target}
    PRIVATE QTBundle
  )
ENDIF()

IF(RV_TARGET_WINDOWS)
  TARGET_LINK_LIBRARIES(
    ${_target}
    PRIVATE win_posix win_pthreads
  )
ENDIF()

IF(RV_TARGET_WINDOWS)
  ADD_LINK_OPTIONS("-SUBSYSTEM:CONSOLE")
ENDIF()

TARGET_COMPILE_OPTIONS(
  ${_target}
  PRIVATE -DGIT_HEAD=\"${RV_GIT_COMMIT_SHORT_HASH}\" -DRELEASE_DESCRIPTION=\"${RV_RELEASE_DESCRIPTION}\"
)

RV_STAGE(TYPE "EXECUTABLE" TARGET ${_target})

ADD_CUSTOM_COMMAND(
  COMMENT "Installing Open RV Packages"
  OUTPUT ${RV_STAGE_PLUGINS_PACKAGES_DIR}/rvinstall ${INSTALLED_RV_PACKAGE_LIST}
  COMMAND $<TARGET_FILE:${_target}> -force -install -add ${RV_STAGE_PLUGINS_DIR} ${RV_PACKAGE_LIST}
  WORKING_DIRECTORY ${RV_STAGE_BIN_DIR}
  DEPENDS ${_target} packages
)

ADD_CUSTOM_TARGET(
  rvinstall ALL
  DEPENDS ${RV_STAGE_PLUGINS_PACKAGES_DIR}/rvinstall
)

ADD_DEPENDENCIES(installed_packages rvinstall)
