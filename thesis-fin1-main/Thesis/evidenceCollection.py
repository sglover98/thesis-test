import subprocess
import glob 
import os

global backsource1
global backsource2 
backsource1 = "/media/OG"
backsource2 = "/media/OG2"

##create md5sums of the source drives
def evidence():    
    def checkMD51():
        
        subprocess.run(["md5sum","/dev/sda1",">","/media/OG"])
        print("md5sums created for installed drive /dev/sda1")
        
    checkMD51()
    
        
    def createIMG():
        subprocess.run(["dd","if=/dev/sda1","of=/media/OG.img", "bs=1k"])
        
        print("image created")  
    createIMG()



    def checkMD52():
        
        subprocess.run(["md5sum","/dev/sda1",">","/media/OG2"])
        
        print("md5sums created for installed drives")

    checkMD52()

        
    

    def lockimg():
            base_dir= "/media" #set base directory
            
            #get all directories from base directory
            dirs = glob.glob(base_dir, recursive=True)
            
            #loop through directories and set permissions
            for directory in dirs:
             try :
                os.chmod(directory, 0o700)
             
             except PermissionError:
                 print("PermissionError: You do not have permission to change the permission bits of the directory")
             
    lockimg()

        





    