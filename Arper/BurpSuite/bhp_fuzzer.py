from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from java.util import List, ArrayList
import random 

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName('Custom Payload Generator')

        callbacks.registerIntruderPayloadGeneratorFactory(self)
        return

    def getGeneratorName(self):
        return 'BHP Payload Factory'
    
    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)
    

class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self.extender = extender
        self.helpers = extender._helpers
        self.attack = attack
        self.max_payloads = 10
        self.num_iterations = 0 

        return 

    # second steps - counter
    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True

    #third steps - next payload
    def getNextPayload(self, current_payload):
        payload = "".join(chr(x) for x in current_payload)
        payload = self.mutate_payload(payload)
        self.num_iterations += 1
        return payload

    #fourth steps - reset next payload
    def reset(self):
        self.num_iterations = 0
        return

    #fifth steps - let's write fuzzer
    def mutate_payload(self, original_payload):
        picker = random.randint(1, 3)
        offset = random.randint(0, len(original_payload)-1)

        front, back = original_payload[:offset], original_payload[offset:]
    #SQL
        if picker == 1:
            front += "'"
    #XSS
        elif picker == 2:
            front += '<script>alert("BHP!");</script>'
    #random chunk of content
        elif picker == 3:
            chunk_length = random.randint(0, len(back)-1)
            repeater = random.randint(1, 10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]
            
        return front + back


        






    
    


        
    
        
    

    