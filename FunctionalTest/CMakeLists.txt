#---------------------------------------------------------------------------
# Copyright 2011 The Open Source Electronic Health Record Agent
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#---------------------------------------------------------------------------

if(SIK_SYSTEM_TESTING)
  # CPRS only runs on Windows, Thus the Sikuli and GUI test will be added only for those types of machines
  if(WIN32)
    file(GLOB SIKULI_FOLDERS ${CMAKE_CURRENT_SOURCE_DIR}/Sikuli/*.sikuli)
    find_program(SIKULI_EXECUTABLE Sikuli-IDE.bat DOC "Path to the Sikul-IDE.bat file" HINTS "C:/Program Files/Sikuli X/" "C:/Program Files (x86)/Sikuli X/" )
    foreach(sikuli ${SIKULI_FOLDERS})
      get_filename_component(sikuli_name "${sikuli}" NAME_WE)
      add_test(FT_${sikuli_name}Sikuli "@SIKULI_EXECUTABLE@" -s -r "${sikuli}")
      set_tests_properties(FT_${sikuli_name}Sikuli PROPERTIES FAIL_REGULAR_EXPRESSION "FindFailed")
    endforeach()
  endif()
endif()

if(RAS_SYSTEM_TESTING)
  file(GLOB packages ${CMAKE_CURRENT_SOURCE_DIR}/RAS/VistA-FOIA/Packages/*)
  find_path(TEST_RESULTS_DIR NAMES DOC "Path to results directory")
  SET(LOG_LEVEL "INFO" CACHE STRING "Logging Level used by OATs internal logger")
  foreach(package ${packages})
    file(GLOB rastests ${package}/*_test.py)
    foreach(rastest ${rastests})
      get_filename_component(rastest_name "${rastest}" NAME_WE)
      configure_file("${CMAKE_CURRENT_SOURCE_DIR}/RAS/RASTest.cmake.in" "${CMAKE_CURRENT_BINARY_DIR}/RAS_${rastest_name}.cmake" @ONLY)
      add_test(RAS_${rastest_name} ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/RAS_${rastest_name}.cmake)
      endforeach()
  endforeach()
endif()

if(SELENIUM_SYSTEM_TESTING)
  message(STATUS "Testing if Selenium_system_testing invoked: true")
  file(GLOB selenium_packages ${CMAKE_CURRENT_SOURCE_DIR}/Selenium/MyHealtheVet_Tester/src/gov/va/myhealthevet/testing/*)
  message(STATUS "selenium packages - " ${selenium_packages})
  find_path(TEST_RESULTS_DIR NAMES DOC "Path to results directory")
  foreach(selenium_package ${selenium_packages})
    file(GLOB selenium_tests ${selenium_package}/*_test*.py)
	message(STATUS "selenium tests - " ${selenium_tests})
    foreach(selenium_test ${selenium_tests})
      get_filename_component(selenium_test_name "${selenium_tests}" NAME_WE)
      configure_file("${CMAKE_CURRENT_SOURCE_DIR}/Selenium/SeleniumTest.cmake.in" "${CMAKE_CURRENT_BINARY_DIR}/Selenium_${selenium_test_name}.cmake" @ONLY)
      add_test(Selenium_${selenium_test_name} ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/Selenium_${selenium_test_name}.cmake)
    endforeach()
  endforeach()
endif()