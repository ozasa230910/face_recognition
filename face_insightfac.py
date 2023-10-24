import insightface
import cv2

# Initialize the insightface model
model = insightface.app.FaceAnalysis()

# Use CPU to perform face analysis
ctx_id = -1

# Prepare the model
model.prepare(ctx_id=ctx_id)

# Capture an image from the webcam

video_capture = cv2.VideoCapture(0)
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
ret, frame = video_capture.read()

# Save the captured image

cv2.imwrite('image/captured_image.jpg', frame)

# Load the image

img = cv2.imread('image/captured_image.jpg')

# Perform face analysis

faces = model.get(img)

# Print the results

for idx, face in enumerate(faces):
	print(f"Face {idx + 1}:")
	print(f"  Age: {face.age}")
	print(f"  Gender: {'Male' if face.gender == 0 else 'Female'}")
	print(f"  Emotion: {face.emotion}")

# 性別、年齢、感情を画像の上部に表示

for idx, face in enumerate(faces):
	org = (10, 20)
	fontFace = cv2.FONT_HERSHEY_SIMPLEX
	fontScale = 0.75
	color = (0, 255, 0)
	thickness = 1
	cv2.putText(img, f"Gender: {'Male' if face.gender == 0 else 'Female'}", org, fontFace, fontScale, color, thickness)
	org = (10, 40)
	cv2.putText(img, f"Age: {face.age}", org, fontFace, fontScale, color, thickness)
	org = (10, 60)
	cv2.putText(img, f"Emotion: {face.emotion}", org, fontFace, fontScale, color, thickness)

# 画像を表示

cv2.imshow('img', img)
cv2.waitKey(0)