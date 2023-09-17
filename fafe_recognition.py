#**************************************
# fece_recongnition 使用
#**************************************

##顔画像を読み込む

imimport streamlit as st
import face_recognition
import matplotlib.pyplot as plt
import glob
import numpy as np


## ******************************************************
# 認証する人の写真を撮り /Authenticator/tatget.jpg と保存する
## ******************************************************
import cv2
from PIL import Image

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
#'''

## ******************************************************
# 認証する（tatget.jpe が　登録墨の人物にあるか）
## ******************************************************

# 保存されている人物の顔の画像を読み込む。
known_face_imgs = []
files = glob.glob("Registered/*")

#登録されている人物を表示
print("＊＊＊登録済者＊＊＊")
for file in files:
        print(file)

# known_face_imgs[] に登録者を格納する
for path in files: 
    #print (path)
    img = face_recognition.load_image_file(path)
    #print("登録済者 = ",img)　#　配列でかくのう
    known_face_imgs.append(img)
    
# 認証する人物の顔の画像を読み込む。
face_img_to_check = face_recognition.load_image_file("Authenticator/target.jpg")

## 顔の領域を検出する
# 顔の画像から顔の領域を検出する。
known_face_locs = []
for img in known_face_imgs:
    #loc = face_recognition.face_locations(img, model="cnn") 
    # model"cnn"はメチャ遅いので"vggface2"にした
    loc = face_recognition.face_locations(img, model="vggface2")
    assert len(loc) == 1, "画像から顔の検出に失敗したか、2人以上の顔が検出されました"
    known_face_locs.append(loc)
#face_loc_to_check = face_recognition.face_locations(face_img_to_check, model="cnn")
face_loc_to_check = face_recognition.face_locations(face_img_to_check, model="vggface2")

assert len(face_loc_to_check) == 1, "画像から顔の検出に失敗したか、2人以上の顔が検出されました"

# 結果を確認するために、matplotlib で顔の領域を画像上に描画する
def draw_face_locations(img, locations):
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_axis_off()
    for i, (top, right, bottom, left) in enumerate(locations):
        # 長方形を描画する。
        w, h = right - left, bottom - top
        ax.add_patch(plt.Rectangle((left, top), w, h, ec="r", lw=2, fill=None))
    plt.show()


for img, loc in zip(known_face_imgs, known_face_locs):
    draw_face_locations(img, loc)
    
draw_face_locations(face_img_to_check, face_loc_to_check)

## 顔の領域から特徴量を抽出する
# 顔の領域から特徴量を抽出する。
known_face_encodings = []
for img, loc in zip(known_face_imgs, known_face_locs):
    (encoding,) = face_recognition.face_encodings(img, loc)
    known_face_encodings.append(encoding)

(face_encoding_to_check,) = face_recognition.face_encodings(
    face_img_to_check, face_loc_to_check)

## マッチする人物がいるかどうかを調べる

matches = face_recognition.compare_faces(known_face_encodings, face_encoding_to_check)
print(matches)  # [True, False, False]

## 特徴量同士の距離を計算する

dists = face_recognition.face_distance(known_face_encodings, face_encoding_to_check)
print(dists)

# 認証されたたか否か　→　matches内に"True#"があるか否か　ある場合：承認　　ない場合：未承認
result = True in matches  # matches内に"True#"があるか否か
#print("result =",result)  # False
if result == True:
    print('認証されました')
else:
    print('認証されません')
       
## 認証された登録済者の表示
for i,True_or_false in enumerate(matches):
    if True_or_false == True:
        im = np.array(Image.open(files[i])) # <class 'PIL.Image.Image'>,3次元配列
        #print(type(im))
        #print("im = ",im)
        img = Image.fromarray(im) # <class 'numpy.ndarray'>,<PIL.Image.Image image mode=RGB size=360x430 at 0x23D508A1B48>.
            #print(type(img))
        #print(i,img)
        
        #保存する画像を表示する
        #画像をarrayに変換False
        im_list = np.asarray(im)
        #貼り付け
        plt.imshow(im_list)
        #X,Y塾」の目盛りを日曲事にする
        plt.xticks([])
        plt.yticks([])
        #表示
        plt.show()