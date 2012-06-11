import os
import subprocess

class ImageProcessor():
    @classmethod
    def exec_command(cls, command):
        """
        Запускает команду в системной оболочке
        """
        print(command)
        child = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE) 
        output = child.stdout.read()
        return output

    @classmethod
    def shrink_2x(cls, img_path):
        """
        Уменьшает изображение img_path и сохраняет его в *_resized.jpg
        """
        new_name = "%s_resized.jpg"%(os.path.splitext(img_path)[0])
        command = "convert -resize 50% {0} {1}".format(img_path, new_name)
        cls.exec_command(command)
        
