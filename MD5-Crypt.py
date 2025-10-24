import itertools
import string
import sys
from passlib.hash import md5_crypt

def crack_md5_crypt_passlib(full_hash, prefix, max_len, charset):
    """
    MD5-Crypt ($1$) ハッシュに対してマスク攻撃を実行します (passlib使用)。

    :param full_hash: /etc/shadow から取得した完全なハッシュ文字列
    :param prefix: パスワードの既知の先頭部分
    :param max_len: パスワードの未知部分の最大長
    :param charset: 未知部分を構成する文字セット
    :return: 発見したパスワード、またはNone
    """
    print(f"\n[INFO] 解析を開始します。プレフィックス: '{prefix}', 未知部分の最大長: {max_len}")

    # 未知部分の長さを1からmax_lenまで試行
    for length in range(1, max_len + 1):
        print(f"[*] 未知部分の長さ {length} の組み合わせを試行中...")
        
        # itertools.productを使用して、指定された長さの文字の組み合わせをすべて生成
        guesses = (''.join(p) for p in itertools.product(charset, repeat=length))

        # 生成された各組み合わせをテスト
        for suffix in guesses:
            guess = prefix + suffix
            
            # passlibのverify関数でパスワード候補とハッシュを比較
            # これにより、ソルトの抽出やハッシュ化のプロセスが内部で処理される
            if md5_crypt.verify(guess, full_hash):
                print("\n" + "="*40)
                print(f" パスワードを発見しました: {guess}")
                print("="*40)
                return guess

    # ループが完了しても見つからなかった場合
    print("\n" + "="*40)
    print(f" 指定された長さの範囲ではパスワードを発見できませんでした。")
    print("="*40)
    return None

if __name__ == "__main__":
    print("="*60)
    print("!!! 法的・倫理的免責事項!!!")
    print("このスクリプトは教育目的、またはあなたが明確な許可を得ている")
    print("システムのセキュリティ監査のためにのみ使用してください。")
    print("許可なく他人のパスワードを解析する行為は違法です。")
    print("="*60)
    print("\nMD5-Crypt ($1$) パスワード解析スクリプト (Windows対応版)\n")

    # ユーザーからの入力を受け取る
    try:
        target_hash = input("解析対象のハッシュ文字列全体を入力してください (例: $1$salt$hash): ")
        if not target_hash.startswith("$1$"):
            print("\n エラー: これはMD5-Crypt形式のハッシュではありません。'$1$'で始まる必要があります。")
            sys.exit(1)

        known_prefix = input("パスワードの既知の先頭部分を入力してください: ")
        
        max_suffix_length_str = input("パスワードの未知部分の最大長を入力してください (例: 4): ")
        max_suffix_length = int(max_suffix_length_str)

    except ValueError:
        print("\n エラー: 未知部分の長さには数値を入力してください。")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[INFO] ユーザーによって処理が中断されました。")
        sys.exit(0)

    # 解析に使用する文字セットを定義
    character_set = string.ascii_letters + string.digits + string.punctuation
    
    print("\n[INFO] 解析に使用する文字セット:")
    print(character_set)

    # 解析関数を実行
    try:
        crack_md5_crypt_passlib(target_hash, known_prefix, max_suffix_length, character_set)
    except KeyboardInterrupt:
        print("\n\n[INFO] ユーザーによって処理が中断されました。")
        sys.exit(0)