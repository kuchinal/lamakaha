#
# Copyright (C) 2022  Autodesk, Inc. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

INCLUDE(cxx_defaults)

SET(_target
    "io_jp2"
)

SET(_sources
    init.cpp
)

ADD_LIBRARY(
  ${_target} SHARED
  ${_sources}
)
SET_TARGET_PROPERTIES(
  ${_target}
  PROPERTIES PREFIX ""
)

TARGET_LINK_LIBRARIES(
  ${_target}
  PRIVATE IOjp2
)

RV_STAGE(TYPE "IMAGE_FORMAT" TARGET ${_target})
