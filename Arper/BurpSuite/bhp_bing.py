#coding: utf-8"
from burp import IBurpExtender
from burp import IContextMenuFactory


from java.net import URL
from java.util import ArrayList
from javax.swing import JMenuItem
from thread import start_new_thread

import json
import socket
import urllib2

api_key = 'lVyEGE8UFSutsrnDTBMrUgaX9437olxw'
api_host = 'api.shodan.io'



class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None    #Menu

        callbacks.setExtensionName('BHP Shodan')
        callbacks.registerContextMenuFactory(self)

        return
    
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem('Send to Shodan', actionPerformed=self.shodan_menu))

        return menu_list
    
    def shodan_menu(self, event):
        http_traffic = self.context.getSelectedMessages()
        print("%d requests highlighted" % len(http_traffic)) #len HTTP-requests

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()

            print('User selected host: %s' % host)
            self.shodan_search(host)

        return 

        
    def shodan_search(self, host):
        try:
            is_ip = bool(socket.inet_aton(host))
        except socket.error:
            is_ip = False

        if is_ip:
            ip_adress = host
        else:
            ip_adress = socket.gethostbyname(host)

        start_new_thread(self.shodan_query, (ip_adress, ))



    def shodan_query(self, ip_adress):
        print('Perfoming Shodan Search for IP: %s' % ip_adress)
        http_requests = 'GET https://%s/shodan/host/%s?key=%s HTTP/1.1\r\n' % (api_host, urllib2.quote(ip_adress), api_key)

        http_requests += 'Host: %s\r\n' % api_host
        http_requests += 'Accept: application/json\r\n'
        http_requests += 'Connection: close\r\n'
        http_requests += 'User-Agent: Black Hat Python\r\n\r\n'

        json_body = self._callbacks.makeHttpRequest(api_host, 443, True, http_requests).tostring()       # send HTTP-request through Burp to API SHODAN/443-port
        json_body = json_body.split('\r\n\r\n', 1)[1]
     
        try:
            response = json.loads(json_body)
        
        except Exception as e:
            print('JSON error: %s' %str(e))   
            
        else:
            if 'data' in response:    #checks if there is 'data' in response.(servise IP)
                for service in response['data']:
                    if 'http' in service.get('product', '').lower():
                        print('*'*100)
                        print('host: %s' % hostname)
                        print('Port: %s' % service['port'])
                        print('Service: %s' % service.get('product', 'N/A'))
                        if 'http' in service:
                            print('Title: %s' % service['http'].get('title', 'N/A'))
                            print('Hostnames: %s' % ', '.join(service['http'].get('hostnames', [])))
                     
                        print('*'*100)

                        if 'http' in service and 'hostnames' in service['http']:
                            for hostname in service['http']['hostnames']:
                                try:
                                    java_url = URL('http://' + hostname)
                                    if not self._callbacks.isInScope(java_url):
                                        print("Adding %s to Burp Scope"% hostname)
                                        self._callbacks.includeInScope(java_url)
                                except:
                                    continue
                    
            else:
                print('No results for ip %s' % ip_adress)
        return
#>>>>>> Not True <<<<<<s
                










                    





    

        




    


    


    

