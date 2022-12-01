"""
This file holds all the constants used in the test files.
"""

import time

# Test Parameters for User
USER_TEST_ID1 = 1
USER_TEST_NAME1 = "Hayden"
USER_TEST_PUBLIC_ID1 = "10101"
USER_TEST_EMAIL1 = "WWU-Wash-And-Dry@outlook.com"
USER_TEST_FLOOR1 = 2
USER_TEST_DORM1 = "Foreman"

# Test Parameters for create machine by id
MACHINE_TEST_PUBLIC_ID1 = 1
MACHINE_TEST_FLOOR_ID1 = 1
MACHINE_TEST_DORM1 = "Sittner"
MACHINE_TEST_FLOOR1 = 1
MACHINE_TEST_STATUS1 = "Free"
MACHINE_TEST_LAST_SERVICE_DATE1 = "10-27-2022"
MACHINE_TEST_INSTALLATION_DATE1 = "10-27-2022"
MACHINE_TEST_FINISH_TIME1 = None
MACHINE_TEST_USER_NAME1 = None

# Test Parameters for get put delete machine by id
MACHINE_TEST_PUBLIC_ID2 = 2
MACHINE_TEST_FLOOR_ID2 = 2
MACHINE_TEST_DORM2 = "Foreman"
MACHINE_TEST_FLOOR2 = 2
MACHINE_TEST_STATUS2 = "Free"
MACHINE_TEST_LAST_SERVICE_DATE2 = "10-27-2022"
MACHINE_TEST_INSTALLATION_DATE2 = "10-27-2022"
MACHINE_TEST_FINISH_TIME2 = None
MACHINE_TEST_USER_NAME2 = None

# Test Parameters for get machine by dorm and floor
MACHINE_TEST_PUBLIC_ID3 = 3
MACHINE_TEST_FLOOR_ID3 = 3
MACHINE_TEST_DORM3 = "Foreman"
MACHINE_TEST_FLOOR3 = 2
MACHINE_TEST_STATUS3 = "Free"
MACHINE_TEST_LAST_SERVICE_DATE3 = "10-27-2022"
MACHINE_TEST_INSTALLATION_DATE3 = "10-27-2022"
MACHINE_TEST_FINISH_TIME3 = None
MACHINE_TEST_USER_NAME3 = None

MACHINE_TEST_PUBLIC_ID4 = 4
MACHINE_TEST_FLOOR_ID4 = 4
MACHINE_TEST_DORM4 = "Foreman"
MACHINE_TEST_FLOOR4 = 2
MACHINE_TEST_STATUS4 = "Free"
MACHINE_TEST_LAST_SERVICE_DATE4 = "10-27-2022"
MACHINE_TEST_INSTALLATION_DATE4 = "10-27-2022"
MACHINE_TEST_FINISH_TIME4 = None
MACHINE_TEST_USER_NAME4 = None

# Test Parameters for get notification
MACHINE_TEST_PUBLIC_ID5 = 5
MACHINE_TEST_FLOOR_ID5 = 5
MACHINE_TEST_DORM5 = "Conard"
MACHINE_TEST_FLOOR5 = 3
MACHINE_TEST_STATUS5 = "In_use"
MACHINE_TEST_LAST_SERVICE_DATE5 = "10-27-2022"
MACHINE_TEST_INSTALLATION_DATE5 = "10-27-2022"
MACHINE_TEST_FINISH_TIME5 = (int(time.time())) // 300
MACHINE_TEST_USER_NAME5 = "Hayden"

# Test Parameters for Emails
RECIPIENTS = ["WWU-Wash-And-Dry@outlook.com"]
BODY = "Testing email"
SUBJECT = "Testing"