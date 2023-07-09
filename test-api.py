import requests

username = input('>>> Enter API username: ')
password = input('>>> Enter API password: ')

session = requests.session()
session.auth = (username, password)

def get_members():
    url = 'http://127.0.0.1:5000/member'
    req = session.get(url=url)
    return req.json()

def get_member(member_id):
    url = f'http://127.0.0.1:5000/member/{member_id}'
    req = session.get(url=url)
    return req.json()

def add_member(name, email, level):
    url = 'http://127.0.0.1:5000/member'
    json = {
        'name': name,
        'email': email,
        'level': level
    }
    req = session.post(url=url, json=json)
    return req.json()

def edit_member(member_id, name, email, level, method):
    url = f'http://127.0.0.1:5000/member/{member_id}'
    json = {
        'name': name,
        'email': email,
        'level': level
    }
    
    if method.lower() == 'put':
        req = session.put(url=url, json=json)
        
    elif method.lower() == 'patch':
        req = session.patch(url=url, json=json)
    
    else:
        return 'Method Not Allowed.'
    
    return req.json()

def delete_member(member_id):
    url = f'http://127.0.0.1:5000/member/{member_id}'
    req = session.delete(url=url)
    return req.json()


while True:
    function = input('Enter Number of function or enter end for stop:\n\t1 - Get all Member.\n\t2 - Get one Member bt ID.\n\t3 - add new Member.\n\t4 - update Member by ID.\n\t5 - Delete Member by ID.\n\t> ')

    if function == '1':
        result = get_members()
        print(f'>>> Result:\n{result}\n\n')

    elif function == '2':
        member_id = input('Enter Member ID: ')
        result = get_member(member_id=member_id)
        print(f'>>> Result:\n{result}\n\n')

    elif function == '3':
        name = input('Enter Member name: ')
        email = input('Enter Member email: ')
        level = input('Enter Member level: ')
        
        result = add_member(name=name, email=email, level=level)
        print(f'>>> Result:\n{result}\n\n')

    elif function == '4':
        member_id = input('Enter Member ID: ')
        name = input('Enter Member name: ')
        email = input('Enter Member email: ')
        level = input('Enter Member level: ')
        method = input('Enter Member method: ')
        
        result = edit_member(member_id=member_id, name=name, email=email, level=level, method=method)
        print(f'>>> Result:\n{result}\n\n')

    elif function == '5':
        member_id = input('Enter Member ID: ')
        
        result = delete_member(member_id=member_id)
        print(f'>>> Result:\n{result}\n\n')
        
    elif function.lower() == 'end':
        break
        
    else:
        print('Not Find Method.\n\n',)

