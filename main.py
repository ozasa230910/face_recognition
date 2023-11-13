# 顔の情報を取得
for i, face in enumerate(response['FaceDetails']):
    # 日本語の文字列を文字コード「UTF-8」でエンコードする
    gender = str(face['Gender']['Value'])
    age_low = str(face['AgeRange']['Low'])
    age_high = str(face['AgeRange']['High'])
    emotion = str(face['Emotions'][0]['Type'])

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
    font = ImageFont.load_default()
    text_position = (left, top)

    # 日本語の描画
    draw.text(text_position, f"性別: {gender}", font=font, fill="white")
    draw.text((text_position[0], text_position[1] + 20), f"年齢: {age_low}-{age_high} 歳", font=font, fill="white")
    draw.text((text_position[0], text_position[1] + 40), f"感情: {emotion}", font=font, fill="white")
