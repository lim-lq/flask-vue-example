# coding=utf-8
"""
desc:   views interface

"""
import students

# url to access Resource
url_patterns = [
    # (Resource, "url pattern", endpoint)
    (students.StudentList, "students", "student_list")
]
