import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np

st.title("Facenet(DeepFace)で顔認識を行い性別、年齢、感情を画像上に表示するプログラム")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # 画像の色温度を調整
    result = DeepFace.analyze(image, actions=['gender', 'age', 'emotion'])
    if isinstance(result, list):
        for i in range(len(result)):
            st.write(f"顔{i+1}")
            st.write("性別: ", result[i]["gender"])
            st.write("年齢: ", result[i]["age"])
            st.write("感情: ", result[i]["dominant_emotion"])
    else:
        st.write("性別: ", result["gender"])
        st.write("年齢: ", result["age"])
        st.write("感情: ", result["dominant_emotion"])
    st.image(image)




