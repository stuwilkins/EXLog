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

#!/usr/bin/python
import time
from EXLog.epicsLogger.smartLog import createLogInstance
client = createLogInstance('sampleinstance')

start_time = time.time()
log_objects = client.findLog(property='sweep', attribute='crystal_name',
value="SNNAT15")
end_time = time.time()
elapsed_time = end_time-start_time
print "retrieval elapsed time = " + str(elapsed_time)

for entry in log_objects:
   for prop_object in entry.getProperties():
     att_names = prop_object.getAttributeNames()
     att_dictionary = prop_object.getAttributes()
     for att_name in att_names:
       print att_name + "=" + att_dictionary[att_name]
end_time = time.time()
elapsed_time = end_time-start_time
print "total elapsed time = " + str(elapsed_time)

---------------
#2 My pxdb->olog transfer program:

from pxdb.models import Sweep
from EXLog.epicsLogger.smartLog import createLogInstance
import time
client = createLogInstance('sampleinstance')
print "getting sweeps with django"
sweep_list=Sweep.objects.filter(timestamp__range=("2012-01-30
00:00:00","2012-07-01 00:00:00"))
print sweep_list[0].id
print "got sweeps"
for i in range (0,len(sweep_list)):
   s = sweep_list[i]
   print s.id
   print s.timestamp
   client.capture('sweep',
timestamp=s.timestamp,rotstart=s.rotstart,rotend=s.rotend,rotinc=s.rotinc,rotaxis=s.rotaxis,exptime=s.exptime,wavelength=s.wavelength,distance=s.dist\
ance,omega=s.omega,kappa=s.kappa,phi=s.phi,two_theta=s.two_theta,directory=s.directory,file_template=s.file_template,numstart=s.numstart,sweep_num=s.sweep_num,images_collected\
=s.images_collected,beamline_id=s.beamline_id,detector_id=s.detector.id,project_id=s.project.id,crystal_name=s.crystal_name,group_auth_id=s.group_auth.id,automount=s.automount\
)
   client.log(description="test from pxdb", owner='olog',
logbooks=["johnLog"])