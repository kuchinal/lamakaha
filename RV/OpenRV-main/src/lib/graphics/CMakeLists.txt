#
# Copyright (C) 2022  Autodesk, Inc. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
ADD_SUBDIRECTORY(TwkGLF)
IF(RV_TARGET_DARWIN)
  ADD_SUBDIRECTORY(TwkGLFCoreGraphics)
ENDIF()
ADD_SUBDIRECTORY(TwkGLFFBO)
