import sys
import os

FREECADPATH = 'C:\\FreeCAD19\\bin' # path to your FreeCAD.so or FreeCAD.dll file
sys.path.append(FREECADPATH)
from django.views.decorators.csrf import csrf_exempt

import FreeCAD
import Part
import Mesh

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import FileResponse

from django.shortcuts import render
from .forms import UploadFileForm

#from somewhere import handle_uploaded_file
def handle_uploaded_file(f):
    #os.remove('C:/inetpub/wwwroot/converter/uploads/loaded.stp')
    #os.remove('C:/inetpub/wwwroot/converter/uploads/converted.stl')
    
    with open('C:/inetpub/wwwroot/converter/uploads/loaded.stp', 'bw+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
# Create your views here.
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        handle_uploaded_file(request.FILES['file'])
        
        shape = Part.Shape()
        shape.read('C:/inetpub/wwwroot/converter/uploads/loaded.stp')
        mesh = Mesh.Mesh()
        mesh.addFacets(shape.tessellate(0.01))
        mesh.write('C:/inetpub/wwwroot/converter/uploads/converted.stl')
        
        response = FileResponse(open('C:/inetpub/wwwroot/converter/uploads/converted.stl', 'rb'))
        response["Access-Control-Allow-Origin"] = "*"
        return response
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

#class HomeView():
#    def post(self, request):
#        shape = Part.Shape()
#        shape.read(request.POST["file"])
#        doc = App.newDocument('Doc')
#        pf = doc.addObject("Part::Feature","MyShape")
#        pf.Shape = shape
#        Mesh.export([pf], 'converted.stl')
#
