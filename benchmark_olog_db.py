__author__ = 'arkilic'
import time
from dummyBroker.Broker import Broker

#Create Broker client and a property called ascan
broker = Broker(session_name='benchmark_olog')
broker.create_property(['ascan'])

#Single ascan dump
start = time.time()
broker.capture('ascan',scan_id=0, start_timestamp='4.7.14', start=0,
               final=100, interval=10, geometry='fourc')

broker.log(description='single ascan dump',logbooks=['CSX'])
end = time.time()
print 'Single scan logging time:' + str(end-start) + ' seconds'

#10 ascan dump
start = time.time()
for i in xrange(10):
    broker.capture('ascan',scan_id=i, start_timestamp='4.7.14', start=0,
               final=100, interval=10, geometry='fourc')
broker.log(description='10 ascan dump',logbooks=['CSX'])
end = time.time()
print '10 buffered scan logging time:' + str(end-start) + ' seconds'


#100 ascan dump
start = time.time()
for i in xrange(100):
    broker.capture('ascan',scan_id=i, start_timestamp='4.7.14', start=0,
               final=100, interval=10, geometry='fourc')
broker.log(description='100 ascan dump',logbooks=['CSX'])
end = time.time()
print '100 buffered scan logging time:' + str(end-start) + ' seconds'
#1000 ascan dump
start = time.time()
for i in xrange(1000):
    broker.capture('ascan',scan_id=i, start_timestamp='4.7.14', start=0,
               final=100, interval=10, geometry='fourc')
broker.log(description='1000 ascan dump',logbooks=['CSX'])
end = time.time()
print '1000 buffered scan logging time:' + str(end-start) + ' seconds'
#10000 ascan dump


#10000 ascan dump




#10 single recursive ascan dumps

#100 single recursive ascan dumps

#1000 single recursive ascan dumps

#10000 single recursive ascan dumps

#100000 single recursive ascan dumps
#