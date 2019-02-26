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

# import models
from django.contrib.auth.models import User
from api.models import Profile, Resume

# import helper
from api.helpers.utility import validator
from fpdf import FPDF


# functions
def createPDFUserData(data):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=data["firstname"]+" "+data["lastname"], ln=1, align="C")
    resume = pdf.output("simple_demo.pdf")


def createPDFProfileBio(data):
    pass


def createPDF(dataType, data):
    switch = {
        "user": createPDFUserData(data),
        "profilebio": createPDFProfileBio(data)
    }
    switch[dataType]


def createUser(reqData):
    data = {
        "email": reqData.POST["email"],
        "password": hash(reqData.POST["password"]),
        "firstname": reqData.POST["firstname"],
        "lastname": reqData.POST["lastname"]
    }

    try:
        user = User.objects.create(
            username=data["firstname"]+" "+data["lastname"],
            email=data["email"],
            password=data["password"],
            first_name=data["firstname"],
            last_name=data["lastname"]
        )

        createPDF("user", data)

        return {
            "type": "USER ADDITION SUCCESS",
            "userid": user.id
        }
    except Exception as e:
        return {
            "type": "USER ADDITION FAILED",
            "error": str(e)
        }


def updateProfileBio(reqData):
    data = {
        "userid": int(reqData.POST["userid"]),
        "birthdate": reqData.POST["birthdate"],
        "location": reqData.POST["location"],
        "about": reqData.POST["about"],
        "profilephoto": reqData.FILES["profilephoto"],
        "portfoliosite": reqData.POST["portfoliosite"],
    }

    try:
        profile = Profile.objects.filter(
            user_id=data["userid"],
        ).update(
            location=data["location"],
            birth_date=data["birthdate"],
            about=data["about"],
            profile_photo=data["profilephoto"],
            portfolio_site=data["portfoliosite"]
        )

        return {
            "type": "USER PROFILE-BIO UPDATION SUCCESS",
            "profileid": Profile.objects.filter(
                user_id=data["userid"],
                ).first().id     
        }
    except Exception as e:
        return {
            "type": "USER PROFILE-BIO UPDATION FAILED",
            "error": str(e)
        }


def getUserAll(reqData):
    pass


def getUser(id, reqData):
    pass


def updateUser(reqData):
    pass


def deleteUser(reqData):
    pass


def validateData(reqData, expected_fields):
    result = {
        "type": True,
        "message": "Successfully validated the input"
    }

    errorDictionary = {
        "email": {
            "type": False,
            "message": "Invalid Email Pattern"
        },
        "firstname": {
            "type": False,
            "message": "Invalid First Name Pattern"
        },
        "lastname": {
            "type": False,
            "message": "Invalid Last Name Pattern"
        },
        "password": {
            "type": False,
            "message": "Password Should be atleast 8 characters long"
        }
    }
    for item in expected_fields:
        if validator(item, reqData.POST[item]):
            continue
        else:
            return errorDictionary[item]

    return result


# Views.
@api_view(['GET', 'POST'])
@csrf_exempt
def register(request):
    if request.method == "POST":
        # return JsonResponse(validateData(request))
        expected_fields = ["email", "firstname", "lastname", "password"]
        validation = validateData(request, expected_fields)
        if validation["type"]:
            return JsonResponse(createUser(request))
        else:
            return JsonResponse({"type": "error", "message": validation["message"]})
    elif request.method == "GET":
        return HttpResponse("This is the registration API. Please goto '/' to view the entire documentation")
    else:   
        return JsonResponse({"type": "Invalid Request"})


@api_view(['POST'])
@csrf_exempt
def profileEducation(request, useremail=None):
    if request.method == "POST":
        pass
    else:   
        return JsonResponse({"type": "Invalid Request"})


@api_view(['POST'])
@csrf_exempt
def profileBio(request, useremail=None):
    if request.method == "POST":
        return JsonResponse(updateProfileBio(request))
    else:   
        return JsonResponse({"type": "Invalid Request"})