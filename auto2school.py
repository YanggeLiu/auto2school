import requests
import time

ti = time.time()
ti = int(round(ti*1000))
ti = str(ti)
url_WAN = 'http://172.16.30.33/drcom/login?callback=dr1602648591624&DDDDD=yourid&upass=password&0MKKey=123456&R1=0&R3=1&R6=0&para=00&v6ip=&_='+ti
Cancel_url_WAN = 'http://172.16.30.33/drcom/logout?callback=dr1602658731495&_='+ti
url_WIFI = 'http://172.16.30.45/drcom/login?callback=dr1602658491651&DDDDD=yourid&upass=password&0MKKey=123456&R1=0&R3=1&R6=0&para=00&v6ip=&_='+ti
Cancel_url_WIFI = 'http://172.16.30.45/drcom/logout?callback=dr1602687706562&_='+ti

def is_connect_edu():
    status_code = requests.get(url_WAN).status_code
    print('get %d from edu' %status_code)
    if status_code == 200:
        print('edu okay')
        return True
    else:
        print('edu error')
        return False


def is_connect_web():
    print('begin...')
    t = requests.get('http://www.baidu.com',timeout=3).text
    if t.find('上网登录页') != -1:
        #print(t)
        print("Can't connect to baidu")
        return False
    else:
        print('get 200 from baidu')
        return True

def main(Go):
    while Go:
        t = requests.get('http://www.baidu.com').text
        if t.find('上网登录页') != -1:
            print('Prepare...')
            try:
                requests.get(Cancel_url_WAN)
            except Exception:
                print('No connect to edu_WAN')
                pass
            time.sleep(2)
            try:
                requests.get(Cancel_url_WIFI,timeout=2)
            except Exception:
                print('No connect to edu_WIFI')
                pass
            if is_connect_edu():
                if not is_connect_web():
                    print('try connect web again')
                    requests.get(Cancel_url_WAN)
                    time.sleep(2)
                    requests.get(url_WIFI)
                    if not is_connect_web():
                        print('try connect web again...')
                        continue
                    else:
                        print('connect to web')
                        break
                else:
                    print('connect to web...')
                    break
            else:
                print('try connect edu again')
                continue
        else:
            Go = False
    else:
        print('No need to connect edu')

if __name__=="__main__":
    Go = True
    main(Go)