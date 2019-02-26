# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

# import rest framework stuff
# from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from rest_framework.decorators import api_view

# to extempt csrf token
from django.views.decorators.csrf import csrf_exempt

# import json
import json

# import models
from api.models import Payslip, EmployeeDetails, EmployeeSalaryDetails

# import a connection
from django.db import connection

# tempelate loader
from django.template.loader import get_template

# to convert query results to json
from django.core import serializers

# utility
from api.utility import pdf
from api.utility.response import success, error
from api.utility.regex import lookup, lookupfieldsmeta, EXPECTED_META


# #### CUSTOM PAYSLIP AND EMPLOYEE FIELD CREATION ####
# Here we check if each field data is entered correctly
def executeQuery(query, retrieve=False, one=False):
    try:
        # create a connection
        cursor = connection.cursor()
        # execute the sql
        cursor.execute(query)

        # if user wants data
        if retrieve:
            # if user wants one data
            if one:
                result = cursor.fetchone()
                cursor.close()
                return result
            else:
                # if user wants all data
                result = cursor.fetchall()
                cursor.close()
                return result
        else:
            # if not then just close the cursor
            cursor.close()
    except Exception as e:
        return str(e)


def queryStringDB(field):
    switch = field["type"]
    boolean_choices = {
        "Yes": "TRUE",
        "No": "FALSE"
    }
    if switch == "Character":
        if lookupfieldsmeta(field['size'], switch, "allowedtype"):
            return "VARCHAR (" + field["size"] + ")"
        else:
            return error("Invalid size paramter for Character")
    elif switch == "Integer":
        return "INTEGER"
    elif switch == "Boolean":
        default = ""
        if lookupfieldsmeta(field["default"], switch, "allowedtype"):
            default = boolean_choices[field["default"]]
        else:
            return error("Invalid Boolean Type. Boolean Types are: 'Yes' or 'No'")
        return "BOOLEAN DEFAULT " + default
    else:
        return error("Invalid Datatype" + switch) 


def createEmployeeField(reqData):
    # first get all the fields in the table
    fields = getEmployeeField()

    for key, value in reqData.items():
        # if the field already exists then do nothing and continue the loop
        if key in fields:
            continue

        sql = "ALTER TABLE api_employeedetails ADD "
        fieldname = key
        qstring = queryStringDB(value)
        sql = sql + fieldname + " " + qstring

        try:
            executeQuery(sql)
        except Exception as e:
            return str(e)


def createEmployeeSalaryField(reqData):
    pass


def updateEmployeeField(reqData):
    # first get all the fields in the table
    fields = getEmployeeField()
    queries = []

    try:
        for key, value in reqData.items():
            # if the field name is valid
            if key in fields:
                # first check for name
                if 'name' in value:
                    # get the new name of the key
                    sql = "ALTER TABLE api_employeedetails RENAME COLUMN " + key + " TO " + value['name']
                    executeQuery(sql)
                # now identify if only the name is to be changed
                # check if the meta tags exist
                if 'meta' in value:
                    # this means that a metga tag exists
                    # which means we will have to change things
                    # a. If type exists,
                            # -> change type
                    # b. Type doesn't exist
                            # -> get type from field
                    # -> meta field must have whatever is required to change type

                    # if there is a name in the data this means,
                    # the name has already been changed so use key name
                    column_name = value['name'] if 'name' in value else key
                    sql = "ALTER TABLE api_employeedetails ALTER COLUMN " + column_name + " TYPE "
                    field_type = ""
                    metatag = ""
                    
                    if 'type' in value['meta']:
                        field_type = value['meta']['type']
                    else:
                        field_type = fields[key].split(" ")[0].capitalize()
                    
                    if field_type in EXPECTED_META:
                        metatag = EXPECTED_META[field_type]
                    else:
                        return error("Incorrect Field Name. Make sure the first letters are capitalized or follow the documentaion for allowed types.")
                    
                    if metatag is None:
                        qstring = queryStringDB({
                            "type": field_type,
                        })
                    else: 
                        qstring = queryStringDB({
                            "type": field_type,
                            metatag: value['meta'][metatag]
                        }) 

                    if 'BOOLEAN' in qstring:
                        qstring = qstring.split(" ")[0]

                    sql = sql + qstring + " USING " + column_name + "::" + qstring.split(" ")[0].lower()
                    queries.append(sql)
                    
                    try:
                        executeQuery(sql)
                    except Exception as e:
                        return error(str(e))     
            else:
                return error("There is no field called " + key)
        return queries
    except Exception as e:
        return error("Invalid data format: " + str(e))


def updateEmployeeSalaryField(reqData):
    pass


# THIS CODE CAN COME IN HANDY SOME TIME
def getEmployeeModelField(reqData, employeeid, date):
    # first check which employer the employeeid belongs to
    employer = lookup(employeeid, "employee")
    token = reqData.META.get('HTTP_TOKEN')
    # based on token, employer and employeeid we will see
    # if the token provided belongs to a the user or not
    # token is to be added as a header

    # if the token is valid then we will return employee field

    # find all the fields
    field_list = filter(
        lambda x: x[0] != '<',
        [str(item) for item in EmployeeDetails._meta.get_fields()]
    )

    # create an empty dictionary
    field_result = {}

    # for each field we find it's type 
    # then we add result to the dictionary
    # with field name as key and its type as value
    for item in field_list:
        field_name = item.split(".")[2]
        field_result[field_name] = str(EmployeeDetails._meta.get_field(field_name).get_internal_type())
    
    return field_result


def getEmployeeField(reqData=None, employeeid=None, date=None):
    # this means that it is called from a GET request
    if reqData is not None:
        # first check which employer the employeeid belongs to
        employer = lookup(employeeid, "employee")
        token = reqData.META.get('HTTP_TOKEN')
        # based on token, employer and employeeid we will see
        # if the token provided belongs to a the user or not
        # token is to be added as a header
        # Here we either return an error or continue below

    # Construct an SQL Query
    sql = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'api_employeedetails'"
    
    # get the result as json
    result = executeQuery(sql, retrieve=True)
    if len(result) == 0:
        return {}
    else:
        fields = {}
        for item in result:
            fields[str(item[0])] = str(item[1])
        return fields


def getEmployeeSalaryField(reqData):
    pass


def deleteEmployeeField(reqData):
    deleteList = reqData["deletefields"]
    # first get all the fields in the table
    fields = getEmployeeField()

    for item in deleteList:
        if item in fields:
            sql = 'ALTER TABLE api_employeedetails DROP COLUMN ' + item
            executeQuery(sql)
        else:
            return error("Invalid database field " + item)


def deleteEmployeeSalaryField(reqData):
    pass


@csrf_exempt
@api_view(['POST', 'PUT', 'DELETE'])
def editEmployeeField(request):
    if request.method == "POST":
        result = createEmployeeField(request.data)
        return JsonResponse({"data": result})
    elif request.method == "PUT":
        result = updateEmployeeField(request.data)
        return JsonResponse({"data": result})
    elif request.method == "DELETE":
        result = deleteEmployeeField(request.data)
        return JsonResponse({"data": result})
    else:
        return JsonResponse(error("Invalid Request Method"))


@csrf_exempt
@api_view(['GET'])
def retrieveEmployeeField(request, employeeid, date):
    return JsonResponse(getEmployeeField(request, employeeid, date))
# #### CUSTOM PAYSLIP AND EMPLOYEE FIELD CREATION  END ####


# #### LATER SECTIONS ####
def createpayslip(reqData):
    pass


def updatepayslip(reqData):
    pass


def getpayslip(company, context):
    try:
        # NOTE: Context should be a dictionary
        templateUrl = company + "_invoice/invoice.html"
        template = get_template()
        html = template.render(context)
        pdf_file = pdf.render_to_pdf(company + "_invoice/invoice.html", context)
        return success(pdf_file)
    except Exception as e:
        return error(str(e))


# creating a payslip
@csrf_exempt
@api_view(['POST', 'PUT'])
def payslipcreate(request):
    # CREATION
    if request.method == "POST":
        try:
            # get the corresponding employee id
            employee_id = EmployeeDetails.objects.filter(
                employee_id=request.data["employeeid"]
            ).first().id

            # create the record in the database
            payslip = Payslip.objects.create(
                employee_id=employee_id,
                absent_days=request.data["absentdays"],
                present_days=request.data["presentdays"],
                days_in_month=request.data["daysinmonth"],
                period=request.data["period"]
            )

            return JsonResponse({
                "status": "SUCCESS",
                "success": json.dumps({
                    "id": payslip.id
                })
            })
        except Exception as e:
            return JsonResponse({
                "status": "ERROR",
                "error": str(e)
            })
        
        return JsonResponse({"id": payslip.id})
    elif request.method == "PUT":
        try:
            # get the corresponding employee id
            employee_id = EmployeeDetails.objects.filter(
                employee_id=request.data["employeeid"]
            ).first().id

            # get all objects with that id
            payslips = [item.id for item in Payslip.objects.filter(
                employee_id=employee_id,
                period=request.data["period"]
            )]

            for item in payslips:
                Payslip.objects.filter(
                    id=item
                ).update(
                    absent_days=request.data["absentdays"],
                    present_days=request.data["presentdays"],
                    days_in_month=request.data["daysinmonth"],
                )

            return JsonResponse({
                "status": "SUCCESS",
                "success": json.dumps({
                    "payslip": payslips
                })
            })
        except Exception as e:
            return JsonResponse({
                "status": "ERROR",
                "error": str(e)
            })
        
        return JsonResponse({"id": payslip.id})
    else:
        return JsonResponse({"type": "method not allowed"})


@csrf_exempt
@api_view(['GET'])
def payslipget(request, employeeid):
    # return render(request, 'invoice/varadhi_invoice.html', {"name": "Namah"})
    return HttpResponse(employeeid)
    
    # employee = lookup(employeeid, "employee")
    # response_pdf = getpayslip()
    # return HttpResponse(pdf_file, content_type="application/pdf")

# ############# TRIAL SPACE ################
# from rest_framework.generics import (
#     ListAPIView,
#     CreateAPIView,
#     RetrieveAPIView
# )

# views
# class PayslipCreateView(CreateAPIView):
    # def get_serializer_class(self):
    #     return JsonResponse({
    #         "type": "test"
    #     })
############ TRIAL SPACE #################
