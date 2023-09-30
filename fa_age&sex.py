#************************************
# 認証に　insightface　を使用
#************************************

import cv2
import numpy as np
import matplotlib.pyplot as plt
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from PIL import Image

## ******************************************************
# 認証する人の写真を撮り /Authenticator/tatget.jped と保存する
## ******************************************************

# カメラの設定　デバイスIDは0
cap = cv2.VideoCapture(0)

# 繰り返しのためのwhile文
picture_num = 1
#'''
while True:
    # カメラからの画像取得
    ret, frame = cap.read()
    
    # 音を鳴らす
    import platform

    def beep(freq, dur=100):
        """
        ビープ音を鳴らす.
        @param freq 周波数
        @param dur  継続時間（ms）
        """
        if platform.system() == "Windows":
            # Windowsの場合は、winsoundというPython標準ライブラリを使います.
            import winsound
            winsound.Beep(freq, dur)
        else:
            # Macの場合には、Macに標準インストールされたplayコマンドを使います.
            import os
            os.system('play -n synth %s sin %s' % (dur/1000, freq))

    # 2000Hzで500ms秒鳴らす
    beep(2000, 500)
    
    # 画像の保存
    #picture_name = 'pic/pic' + str(picture_num) + '.jpg'
    picture_name = 'Authenticator/target' +  '.jpg'
    cv2.imwrite(picture_name, frame)
    picture_num = picture_num + 1

    # カメラの画像の出力
    cv2.imshow('camera' , frame)
    #img = Image.open('pic/target.jpeg' ) 
    #img.show()
    
    #繰り返し分から抜けるためのif文
    if picture_num ==2:
        break

# メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()

## ******************************************************
# 撮った写真から性別、年齢を推定する
## ******************************************************
#'''
#files = ["./image/a.png","./image/b.png","./image/c.png","./image/126.png","./image/127.png"]
files = ["Authenticator/target.jpg"]
j = 0
for f in files:
    app = FaceAnalysis()
    app.prepare(ctx_id=0, det_size=(640,640))
    img = cv2.imread(f)
    faces = app.get(img)
    print('----------------------------------------')
    j = j + 1
    for i in faces:
      if i['gender'] == 1:
          i['gender'] = "男性"
      else:
          i['gender'] = "女性"
      #print('face number:', j)
      print('性別：', i['gender'])
      print('推定年齢：', i['age'])
    rimg = app.draw_on(img, faces)
    plt.imshow(cv2.cvtColor(rimg, cv2.COLOR_BGR2RGB))
    plt.show()