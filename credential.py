import requests
import json
import sys
import os

base = os.path.join(os.path.dirname(os.path.abspath(__file__)),'')

def chk_(url):
    if url[:5] != 'https':
        return 'https://' + url
    else:
        return url

def per(i):
    follow = int(i / 4)
    write = int(i % 4 / 2)
    read = int(i % 4 % 2 / 1)
    per = ''
    if read:
        per += 'read'
    if write:
        per += ' write'
    if follow:
        per += ' follow'
    return per

def register(instance, *args):
    instance = chk_(instance)
    client_name = input('Please input your client name: (default: credential_generator) ')
    if client_name == '':
        client_name = 'credential_generator'
    if args:
        p = per(args[0])
    else:
        p = per(1)
    data = {'client_name': client_name,'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob', 'scopes': p}
    r = requests.post(instance+'/api/v1/apps', data=data)
    rdata = r.json()
    client_id = rdata['client_id']
    client_secret = rdata['client_secret']
    import webbrowser
    p = p.replace(' ','%20')
    webbrowser.open(instance+'/oauth/authorize?client_id='+client_id +'&redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=code&scope='+p)
    code = input('input you code from browser: ')
    print('your access_code is: '+code)
    auth_data = {'client_id': client_id, 'client_secret': client_secret, 'code': code,'grant_type': 'authorization_code', 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'}
    rauth = requests.post(instance + '/oauth/token', data=auth_data)
    access_token = rauth.json()['access_token']
    username = json.loads(requests.get(instance+'/api/v1/accounts/verify_credentials',headers={'Authorization': 'Bearer '+access_token}).content)['acct']
    user = {}
    user[username] = access_token
    login = {}
    login[instance] = user
    file_name = input('Set filename: (default: cred.json)')
    if file_name == '':
        file_name = 'cred.json'
    elif not file_name.endswith('.json'):
        file_name += '.json'
    with open(base + file_name, 'w') as fw:
        json.dump(login, fw)
    return 0

def retrieve(username, instance, filename):
    import os
    instance = chk_(instance)
    if not filename.endswith('.json'):
        filename += '.json'
    with open(base + filename) as f:
        cred = json.load(f)
    if instance in cred:
        if username in cred[instance]:
            return cred[instance][username]
        else:
            return register(instance)
    else:
        return register(instance)

def delcred(username, instance):
    instance = chk_(instance)
    fn = input('please input filename of credential: ')
    if not fn.endswith('.json'):
        fn += '.json'
    with open(base + fn) as fr:
        cred = json.load(fr)
    try:
        cred[instance].pop(username)
        if len(cred[instance]) == 0:
            cred.pop(instance)
    except:
        print('matching user credential not found')
    with open(base + fn, 'w') as f:
        json.dump(cred,f)

if __name__=='__main__':
    action = sys.argv[1]
    if action == 'register':
        inst = input('please input your instance address: ')
        sc = input('please input scope in unix permission: (default: 1)')
        if sc == '':
            sc = 1
        else:
            try:
                sc = int(sc)
            except:
                print('only int is accepted for scope')
                raise ValueError
        register(inst, sc)
    elif action == 'delete':
        try:
            username = sys.argv[2]
            instance = sys.argv[3]
            delcred(username, instance)
        except:
            username = input('please input your username: ')
            instance = input('please input your instance address: ')
            delcred(username, instance)
    else:
        print('input action')
        raise ValueError
