import streamlit as st
import boto3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO  # 追加
from botocore.exceptions import NoCredentialsError

# AWSの認証情報を設定
aws_access_key_id = "AKIAWYMK2ENNUZCMN64I"
aws_secret_access_key = "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"

# AWS Rekognitionの設定
rekognition = boto3.client('rekognition',
                          region_name='ap-northeast-1',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

# Streamlitアプリケーションの設定
st.title("AWS Rekognition 顔認識")

# 画像をアップロード
uploaded_image = st.file_uploader("画像を選択してください...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    try:
        # 画像を表示
        image = Image.open(uploaded_image)
        st.image(image, caption="アップロードされた画像", use_column_width=True)

        # Rekognitionで顔認識を実行
        with st.spinner("解析中..."):
            image_binary = BytesIO(uploaded_image.getvalue())  # 追加
            response = rekognition.detect_faces(
                Image={'Bytes': image_binary.read()},  # 修正
                Attributes=['ALL']
            )

        # 顔が検出された場合
        if response['FaceDetails']:
            # 顔の情報を取得
            for i, face in enumerate(response['FaceDetails']):
                # ... (以前のコードと同じ)

            # 描画された画像を表示
            st.image(image, caption="解析結果", use_column_width=True)
        else:
            st.warning("アップロードされた画像に顔が検出されませんでした。")

    except NoCredentialsError:
        st.error("AWSの認証情報が正しく設定されていません。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
