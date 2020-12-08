import os

def findAllFile(base):
    wjlist=[]
    for dirname,_,i in os.walk(base):
        for wjname in i:
            newdirname=dirname.replace("vod", "vod-play", 1)
            newdirname=dirname.replace("A02", "test2", 1)
            if wjname.endswith('.mp4') or wjname.endswith('.flv'):
                print ('ffmpeg -i '+wjname+' -b:v 800k -b:a 64k '+os.path.join(newdirname,wjname))
    return wjlist        
if __name__ == '__main__':
    base=r"D:\app\Vod_Management\vod"
    wjlist=findAllFile(base)