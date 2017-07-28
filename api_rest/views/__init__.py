# coding=utf-8
"""
desc:   views interface

"""
import students
import admin

# url to access Resource
url_patterns = [
    # (Resource, "url pattern", endpoint)
    (students.StudentList, "students", "student_list")
]
url_patterns.extend(admin.url_patterns)
