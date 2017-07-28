# coding=utf-8
"""
desc:   学生接口模块

"""
from flask import g
from flask_restful import Resource
from flask_restful import reqparse

from api_rest.models import Students
from api_rest.decorators import login_required
from api_rest.http_responses import HTTP_200_OK
from api_rest.privileges import student_manage

add_student_parser = reqparse.RequestParser()
add_student_parser.add_argument("name", required=True)


class StudentList(Resource):
    decorators = [login_required]

    def get(self):
        students = [stu.to_dict() for stu in Students.query.all()]

        return HTTP_200_OK(msg={"students": students})

    @student_manage.required
    def post(self):
        args = add_student_parser.parse_args()
        student = Students(args.name)

        g.db.add(student)
        g.db.commit()
