from django.conf.urls import url

# views
from api import views

urlpatterns = [
    url(
        'employeefield/edit',
        views.editEmployeeField,
        name="employeefield_create"
    ),
    url(
        r'^employeefield/(?P<employeeid>\S+)/(?P<date>\S+)/?',
        views.retrieveEmployeeField,
        name="employeefield_get"
    ),
    url(
        'create/',
        views.payslipcreate,
        name="payslip_create"
    ),
    url(
        r'^(?P<employeeid>\S+)/',
        views.payslipget,
        name="payslip_get"
    )
]