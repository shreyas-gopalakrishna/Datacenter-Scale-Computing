from openalpr import Alpr
alpr = Alpr('us', '/etc/openalpr/openalpr.conf', '/usr/share/openalpr/runtime_data')
results = alpr.recognize_file('beetle.jpg')
if len(results['resluts']) == 0:
    print("Can't find a plate")
else:
    print("Most likely plate is", results['results'][0]['plate'])