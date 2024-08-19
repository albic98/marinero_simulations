# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_marinero_simulations_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED marinero_simulations_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(marinero_simulations_FOUND FALSE)
  elseif(NOT marinero_simulations_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(marinero_simulations_FOUND FALSE)
  endif()
  return()
endif()
set(_marinero_simulations_CONFIG_INCLUDED TRUE)

# output package information
if(NOT marinero_simulations_FIND_QUIETLY)
  message(STATUS "Found marinero_simulations: 0.0.0 (${marinero_simulations_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'marinero_simulations' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${marinero_simulations_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(marinero_simulations_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${marinero_simulations_DIR}/${_extra}")
endforeach()
