from dnslib import DNSRecord, DNSHeader, QTYPE, RR, A
# from dnslib import DNSQuestion, AAAA
from dnslib.server import DNSServer, DNSHandler, BaseResolver
import redis
from os import getenv

env = getenv("REDIS_HOST")
RedisHost = env if env else "127.0.0.1"
env = getenv("REDIS_PORT")
RedisPort = env if env else 6379
RedisPort = int(RedisPort)
env = getenv("REDIS_DB")
RedisDB = env if env else 0
RedisDB = int(RedisDB)
RedisPasswd = getenv("REDIS_PASSWORD")

env = getenv("DNS_HOST")
DNSHost = env if env else "0.0.0.0"
env = getenv("DNS_PORT")
DNSPort = env if env else 53
DNSPort = int(DNSPort)

# RedisHost = "172.16.0.23"
# RedisPort = 30126
# RedisDB = 0
# RedisPasswd = "secret"
# DNSHost = "0.0.0.0"
# DNSPort = 53

REDIS = redis.StrictRedis(host=RedisHost, port=RedisPort, db=RedisDB, password=RedisPasswd)

class MyResolver(BaseResolver):
    ### Data in Variable
    # DNS_RECORDS = {
    #     "example.com": "127.0.0.1",
    #     "meca.local": "192.168.0.1",
    # }

    @classmethod
    def find_record(cls, qname, qtype):
        global REDIS
        domain = qname.rsplit('.', 1)[0]
        if qtype == QTYPE.A:
            ### Data in Redis: set example.com 127.0.0.1
            return REDIS.get(domain).decode()
            ### Data in Variable
            # return cls.DNS_RECORDS[qname]
        return None

    def resolve(self, request, handler):
        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1),
                          q=request.q)

        if request.header.qr == 0:
            ttl = 60
            answer = 0
            for question in request.questions:
                qname = str(question.qname)
                qtype = question.qtype
                rdata = self.find_record(qname, qtype)
                
                if rdata is not None:
                    answer = answer + 1
                    if qtype == QTYPE.A:
                        reply.add_answer(RR(qname, QTYPE.A, ttl=ttl, rdata=A(rdata), rclass=1))
                    # elif qtype == QTYPE.AAAA:
                    #     reply.add_answer(RR(qname, QTYPE.AAAA, ttl=ttl, rdata=AAAA(rdata), rclass=1))
            if answer > 0:
                return reply
        return None
    

# Create DNS server
resolver = MyResolver()
handler = DNSHandler
server = DNSServer(resolver, port=DNSPort, address=DNSHost)

try:
    server.start()
except KeyboardInterrupt:
    pass
finally:
    server.stop()