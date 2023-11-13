import streamlit as st
import boto3
from PIL import Image, ImageDraw, ImageFont
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
            response = rekognition.detect_faces(
                Image={'Bytes': uploaded_image.getvalue()},
                Attributes=['ALL']
            )

        # 顔が検出された場合
        if response['FaceDetails']:
            # 顔の情報を取得
            for i, face in enumerate(response['FaceDetails']):
                gender = face['Gender']['Value']
                age_low = face['AgeRange']['Low']
                age_high = face['AgeRange']['High']
                emotion = face['Emotions'][0]['Type']

                # 顔の位置を取得
                bounding_box = face['BoundingBox']
                image_width, image_height = image.size
                left, top, width, height = (
                    int(bounding_box['Left'] * image_width),
                    int(bounding_box['Top'] * image_height),
                    int(bounding_box['Width'] * image_width),
                    int(bounding_box['Height'] * image_height)
                )

                # 画像に情報を描画
                draw = ImageDraw.Draw(image)

                # 日本語に対応したフォントを指定
                font_path = "C:/Windows/Fonts/meiryo.ttc"  # 例としてメイリオを指定
                font = ImageFont.truetype(font_path, 18)  # フォントサイズは適宜変更

                text_position = (left, top)

                # 日本語の描画
                draw.text(text_position, f"性別: {gender}", font=font, fill="white")
                draw.text((text_position[0], text_position[1] + 20), f"年齢: {age_low}-{age_high} 歳", font=font, fill="white")
                draw.text((text_position[0], text_position[1] + 40), f"感情: {emotion}", font=font, fill="white")

            # 描画された画像を表示
            st.image(image, caption="解析結果", use_column_width=True)
        else:
            st.warning("アップロードされた画像に顔が検出されませんでした。")

    except NoCredentialsError:
        st.error("AWSの認証情報が正しく設定されていません。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
