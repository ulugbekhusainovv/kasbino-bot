# API dan foydalanish
import requests
import json
from data.config import URL as api_url

URL = f'{api_url}/f04b9654-72d1-46fe-8d65-e595ef2dda85'


def get_user(telegram_id):
    try:
        response = requests.get(url=f"{URL}/get_user/", data={'telegram_id': telegram_id})
        if response.status_code == 204:
            return 'Not Found'
        else:
            return json.loads(response.text)
    except:
        pass

def get_employee(telegram_id):
    try:
        response = requests.get(url=f"{URL}/get_employee/",
                                 data={'telegram_id':telegram_id})
        if response.status_code == 204:
            return 'Not Found'
        else:
            return json.loads(response.text)
    except Exception as e:
        return e
# def get_employee(telegram_id):
#     try:
#         response = requests.get(url=f"{URL}/get_employee/", params={'telegram_id': telegram_id})
#         if response.status_code == 200:
#             return json.loads(response.text)
#         elif response.status_code == 204:
#             return 'Not Found'
#         else:
#             return f"Error: {response.status_code}"
#     except Exception as e:
#         return f"Exception: {e}"




def get_employee_by_id(employee_id):
    try:
        response = requests.get(url=f"{URL}/employees/{employee_id}/")
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None
    except:
        pass
# print(get_employee_by_id(1))

def create_user(telegram_id,full_name:str):
    try:
        data = {
            'telegram_id': telegram_id,
            'full_name': full_name,
        }
        response = requests.post(url=f"{URL}/botuser/", json=data)
        if response.status_code == 201:
            return json.loads(response.text)
        else:
            return {}
    except:
        return {}
    

    
def get_all_users():
    try:
        response = requests.get(url=f"{URL}/botuser/")
        return json.loads(response.text)
    except:
        return []
    
def get_company_info():
    try:
        response = requests.get(url=f"{URL}/company-info/")
        return json.loads(response.text)
    except:
        return []


def get_company_structures():
    try:
        response = requests.get(url=f"{URL}/company-structure/")
        return json.loads(response.text)
    except:
        return []


def get_all_employee():
    try:
        response = requests.get(url=f"{URL}/employees/")
        return json.loads(response.text)
    except:
        return []


def get_admin_employees():
    all_employees = get_all_employee()
    admin_employees = [employee for employee in all_employees if employee.get('position') == 'admin']
    return admin_employees



def get_manager_employees():
    all_employees = get_all_employee()
    admin_employees = [employee for employee in all_employees if employee.get('position') == 'manager']
    return admin_employees


def set_all_employee_change_status():
    try:
        employees = get_all_employee()
        for employee in employees:
            employee['status'] = False
            employee_id = employee['id']
            update_response = requests.patch(url=f"{URL}/employees/{employee_id}/", json={'status': False})
            if update_response.status_code == 200:
                get_all_employee()
            else:
                print(f"Failed to set Employee {employee_id} status to False. Status code: {update_response.status_code}")
    except:
        pass

def set_employee_status(employee_id, new_status=True):
    try:
        update_response = requests.patch(url=f"{URL}/employees/{employee_id}/", json={'status': new_status})
        if update_response.status_code == 200:
            return json.loads(update_response.text)
        else:
            return {"error": f"Failed to set Employee {employee_id} status. Status code: {update_response.status_code}"}
    except Exception as e:
        return {"error": f"Error while updating employee status: {e}"}


    # done
def get_all_task():
    try:
        response = requests.get(url=f"{URL}/tasks/")
        return json.loads(response.text)
    except:
        return []


def get_task(id):
    try:
        response = requests.get(url=f"{URL}/get_task/",
                                 data={'id':id})
        if response.status_code == 204:
            return 'Not Found'
        else:
            return json.loads(response.text)
    except:
        return {}

def update_task_status(task_id, new_status):
    api_url = f"{URL}/update_task_status/{task_id}/"
    data = {'new_status': new_status}
    response = requests.put(api_url, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Error updating task status: {response.status_code}, {response.text}"}


def update_task_accepted(task_id, employee_id):
    api_url = f"{URL}/update_task_accepted/{task_id}/"
    data = {'employee_id': employee_id}
    response = requests.put(api_url, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Error updating task accepted: {response.status_code}, {response.text}"}



def get_all_advance():
    try:
        response = requests.get(url=f"{URL}/advances/")
        return json.loads(response.text)
    except:
        return []
    
def get_advance(id):
    try:
        response = requests.get(url=f"{URL}/get_advance/",
                                 data={'id':id})
        if response.status_code==206:
            return json.loads(response.text)
        else:
            return {}
    except:
        return {}

def post_advance(desc, amount, employee_id):
    try:
        data = {
            'desc': desc,
            'amount': amount,
            'employees': employee_id
        }
        response = requests.post(url=f"{URL}/get_advance/", json=data)
        if response.status_code == 201:
            return json.loads(response.text)
        else:
            return {}
    except:
        return {}


    # done

def get_all_offer():
    try:
        response = requests.get(url=f"{URL}/offers/")
        return json.loads(response.text)
    except:
        return []
    
def get_offer(id):
    try:
        response = requests.get(url=f"{URL}/get_offer/",
                                 data={'id':id})
        if response.status_code==206:
            return json.loads(response.text)
        else:
            return {}
    except:
        return {}

def post_offer(desc, employee_id, add_date):
    try:
        data = {
            'desc': desc,
            'employees': employee_id,
            'add_date': add_date
        }
        response = requests.post(url=f"{URL}/get_offer/", json=data)
        if response.status_code == 201:
            return json.loads(response.text)
        else:
            return {}
    except:
        return {}

    # done
def get_all_complaint():
    try:
        response = requests.get(url=f"{URL}/complaints/")
        return json.loads(response.text)
    except:
        return []
    
def get_complaint(id):
    try:
        response = requests.post(url=f"{URL}/get_complaint/",
                                 data={'id':id})
        if response.status_code==206:
            return json.loads(response.text)
        else:
            return {}
    except:
        return {}
    
def post_complaint(desc, employee_id, add_date):
    try:
        data = {
            'desc': desc,
            'employees': employee_id,
            'add_date': add_date
        }
        response = requests.post(url=f"{URL}/get_complaint/", json=data)
        if response.status_code == 201:
            return json.loads(response.text)
        else:
            return {}
    except:
        return {}
    
def post_attendance(employee_id):
    try:
        data = {
            'employee': employee_id
        }
        response = requests.post(url=f"{URL}/attendances/", json=data)
        if response.status_code == 201:
            return json.loads(response.text)
        else:
            return {}
    except:
        return {}