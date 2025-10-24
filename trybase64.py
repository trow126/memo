import base64
import binascii

def decode_base64_string(encoded_str):
    """
    Base64エンコードされた文字列をデコードします。

    :param encoded_str: Base64エンコードされた文字列
    :return: デコードされた文字列、またはエラーメッセージ
    """
    try:
        # Base64文字列はバイト型である必要があるため、ASCIIにエンコード
        encoded_bytes = encoded_str.encode('ascii')
        
        # Base64デコードを実行
        decoded_bytes = base64.b64decode(encoded_bytes)
        
        # デコードされたバイト型データを人間が読める文字列に変換 (UTF-8を想定)
        decoded_str = decoded_bytes.decode('utf-8')
        
        return decoded_str
        
    except binascii.Error:
        # パディングが正しくない場合などのエラーを捕捉
        return "エラー: 入力された文字列のパディングが正しくないか、Base64形式ではありません。"
    except UnicodeDecodeError:
        # デコード後のデータがテキストではない場合
        return f"デコード成功（バイナリデータ）: {decoded_bytes}"
    except Exception as e:
        return f"予期せぬエラーが発生しました: {e}"

if __name__ == "__main__":
    # デコードしたい文字列を入力
    # 例: 'SGVsbG8sIFdvcmxkIQ==' は 'Hello, World!' になります
    input_string = input("デコードしたいBase64文字列を入力してください: ")

    # 関数を呼び出して結果を表示
    result = decode_base64_string(input_string)
    
    print("\n--- 結果 ---")
    print(result)
