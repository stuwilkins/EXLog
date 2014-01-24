__author__ = 'arkilic'
from EXLog.epicsLogger.smartLog import createLogInstance
client = createLogInstance('sampleinstance')
client.createProperty('sweep',{'id':None,
                               'timestamp':None,
                               'rotstart':None,
                               'rotend':None,
                               'rotinc':None,
                               'rotaxis':None,
                               'exptime':None,
                               'wavelength':None,
                               'distance':None,
                               'omega':None,
                               'kappa':None,
                               'phi':None,
                               'two_theta':None,
                               'directory':None,
                               'file_template':None,
                               'numstart':None,
                               'zinger_correct':None,
                               'binned_data':None,
                               'sweep_num':None,
                               'images_collected':None,
                               'notations':None,
                               'beamline_id':None,
                               'detector_id':None,
                               'project_id':None,
                               'crystal_name':None,
                               'group_auth_id':None,
                               'automount':None,
                               'edna':None,
                               'spec':None,
                               'x_roi':None,
                               'y_roi':None,
                               'spec_angle_offset':None,
                               'spec_align_x':None,
                               'spec_align_y':None})
client.capture('sweep', x_roi='some roi')
client.log(description="Entered directory for John Skinner's code", owner='skinner', logbooks=["skinner's logbook"])
log_objects = client.findLog(property='sweep', attribute='y_roi', value="35")
client.capture('sweep', x_roi='11', y_roi='35')
client.log(description="Addition to use case", owner='arkilic', logbooks=["skinner's logbook"])
print client.findLog(property='sweep', attribute='x_roi', value='35')
print client.findLog(property='sweep', attribute='x_roi', value='5')[0].getProperties()[0].getAttributeValue('x_roi')
