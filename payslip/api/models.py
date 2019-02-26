# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class EmployeeDetails(models.Model):
    # employee bio
    name = models.CharField(max_length=250, null=False)

    def __str__(self):
        return self.name
   

class Payslip(models.Model):
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.name
   

class EmployeeSalaryDetails(models.Model):
    employee = models.OneToOneField(EmployeeDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.name
    

    
    


