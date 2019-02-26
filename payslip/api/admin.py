# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api.models import EmployeeDetails, EmployeeSalaryDetails, Payslip


# Register your models here.
admin.site.register(EmployeeDetails)
admin.site.register(EmployeeSalaryDetails)
admin.site.register(Payslip)
