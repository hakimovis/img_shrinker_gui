import os
import subprocess

class ImageProcessor():
    @classmethod
    def exec_command(cls, command):
        print(command)
        child = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE) 
        output = child.stdout.read()
        return output

    @classmethod
    def shrink_2x(cls, img_path):
        new_name = "%s_resized.jpg"%(os.path.splitext(img_path)[0])
        command = "convert -resize 50% {0} {1}".format(img_path, new_name)
        cls.exec_command(command)
        
