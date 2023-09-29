#************************************
# 認証に　aws boto3　を使用 動画　"q"で停止
#************************************

#出典：https://qiita.com/G-awa/items/477f2324552cb908ecd0

import cv2
import boto3
from botocore.config import Config
config = Config(region_name='ap-northeast-1')
s3 = boto3.client('s3', config=config)

# スケールや色などの設定
scale_factor = .15
green = (0,255,0)
red = (0,0,255)
frame_thickness = 2
cap = cv2.VideoCapture(0)
rekognition = boto3.client('rekognition')

# フォントサイズ
fontscale = 1.0
# フォント色 (B, G, R)
color = (0, 120, 238)
# フォント
fontface = cv2.FONT_HERSHEY_DUPLEX

# q を押すまでループします。
while(True):

    # フレームをキャプチャ取得
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # jpgに変換 画像ファイルをインターネットを介してAPIで送信するのでサイズを小さくしておく
    small = cv2.resize(frame, (int(width * scale_factor), int(height * scale_factor)))
    ret, buf = cv2.imencode('.jpg', small)

    # Amazon RekognitionにAPIを投げる
    faces = rekognition.detect_faces(Image={'Bytes':buf.tobytes()}, Attributes=['ALL'])

    # 顔の周りに箱を描画する
    for face in faces['FaceDetails']:
        smile = face['Smile']['Value']
        cv2.rectangle(frame,
                      (int(face['BoundingBox']['Left']*width),
                       int(face['BoundingBox']['Top']*height)),
                      (int((face['BoundingBox']['Left']+face['BoundingBox']['Width'])*width),
                       int((face['BoundingBox']['Top']+face['BoundingBox']['Height'])*height)),
                      green if smile else red, frame_thickness)
        emothions = face['Emotions']
        i = 0
        for emothion in emothions:
            cv2.putText(frame,
                        #str(emothion['Type']) + ": " + str(emothion['Confidence']),
                        str(emothion['Type'].replace('Angry', '怒り').replace('Disgust', '嫌悪').replace('Fear', '恐怖').replace('Happy', '喜び').replace('Sad', '悲しみ').replace('Surprise', '驚き')) + ": " + str(emothion['Confidence']),
                        (25, 40 + (i * 25)),
                        fontface,
                        fontscale,
                        color=green)
           
            i += 1      
    
    # 結果をディスプレイに表示
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
