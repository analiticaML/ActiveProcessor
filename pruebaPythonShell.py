import os
os.system('aws rekognition list-stream-processors --region us-east-1')
from subprocess import call
call('aws rekognition list-stream-processors --region us-east-1', shell=True)




