import random

kana = [
    ["あ", "ア", "a"],
    ["い", "イ", "i"],
    ["う", "ウ", "u"],
    ["え", "エ", "e"],
    ["お", "オ", "o"],
    ["き", "キ", "ki"],
    ["し", "シ", "shi"],
    ["ち", "チ", "chi"],
    ["ひ", "ヒ", "hi"],
    ["か", "カ", "ka"],
    ["く", "ク", "ku"],
    ["け", "ケ", "ke"],
    ["こ", "コ", "ko"],
    ["さ", "サ", "sa"],
    ["す", "ス", "su"],
    ["せ", "セ", "se"],
    ["そ", "ソ", "so"],
    ["た", "タ", "ta"],
    ["つ", "ツ", "tsu"],
    ["て", "テ", "te"],
    ["と", "ト", "to"],
    ["は", "ハ", "ha"],
    ["ふ", "フ", "fu"],
    ["へ", "ヘ", "he"],
    ["ほ", "ホ", "ho"],
    ["ま", "マ", "ma"],
    ["み", "ミ", "mi"],
    ["む", "ム", "mu"],
    ["め", "メ", "me"],
    ["も", "モ", "mo"],
    ["な", "ナ", "na"],
    ["に", "ニ", "ni"],
    ["ぬ", "ヌ", "nu"],
    ["ね", "ネ", "ne"],
    ["の", "ノ", "no"],
    ["や", "ヤ", "ya"],
    ["ゆ", "ユ", "yu"],
    ["よ", "ヨ", "yo"],
    ["わ", "ワ", "wa"],
    ["ゐ", "ヰ", "wi"],
    ["ゑ", "ヱ", "we"],
    ["を", "ヲ", "wo"],
    ["ん", "ン", "n"],
    ["ぎ", "ギ", "gi"],
    ["じ", "ジ", "ji"],
    ["ぢ", "ヂ", "dji"],
    ["び", "ビ", "bi"],
    ["ぴ", "ピ", "pi"],
    ["が", "ガ", "ga"],
    ["ぐ", "グ", "gu"],
    ["げ", "ゲ", "ge"],
    ["ご", "ゴ", "go"],
    ["ざ", "ザ", "za"],
    ["ず", "ズ", "zu"],
    ["ぜ", "ゼ", "ze"],
    ["ぞ", "ゾ", "zo"],
    ["だ", "ダ", "da"],
    ["づ", "ヅ", "dzu"],
    ["で", "デ", "de"],
    ["ど", "ド", "do"],
    ["ば", "バ", "ba"],
    ["ぶ", "ブ", "bu"],
    ["べ", "ベ", "be"],
    ["ぼ", "ボ", "bo"],
    ["ぱ", "パ", "pa"],
    ["ぷ", "プ", "pu"],
    ["ぺ", "ペ", "pe"],
    ["ぽ", "ポ", "po"],
]


def random_kana():
    idx = random.randint(0, len(kana) - 1)
    res = kana[idx].copy()
    # reduce the probability of archaic form of we and wi occuring
    if idx == 39 or idx == 40:
        idx = random.randint(0, len(kana) - 1)
        res = kana[idx].copy()
    # characters with small ya/yu/yo attachable
    if (
        4 < idx < 9 or idx == 26 or idx == 31 or 42 < idx < 48
    ) and random.random() < 0.15:
        # reduce the probability of dji gets modified
        if idx == 45 and random.random() < 0.6:
            pass
        # (very rare) shi, chi => she, che
        elif (idx == 6 or idx == 7) and random.random() < 0.15:
            res[0] += "ぇ"
            res[1] += "ェ"
            res[2] = "she" if idx == 6 else "che"
        else:
            y = random.choice([["ゃ", "ャ", "ya"], ["ゅ", "ュ", "yu"], ["ょ", "ョ", "yo"]])
            res[0] = res[0] + y[0]
            res[1] = res[1] + y[1]
            res[2] = res[2][:-1]  # romaji, strip the last character
            if len(res[2]) == 2:  # if shi, chi or dji
                res[2] += y[2][-1]  # attach only the vowel (a/u/o) => sha/shu/sho
            else:
                if res[2] == "j":  # if ji
                    res[2] += y[2][-1]  # then attach only the vowel (a/u/o) => ja/ju/jo
                else:
                    res[2] += y[2]  # attach the entire ya/yu/yo => gya/gyu/gyo
    # u and fu
    if (idx == 2 or idx == 22) and random.random() < 0.15:
        if idx == 2:
            # u => we, wi
            v = random.choice([["ぃ", "ィ", "i"], ["ぇ", "ェ", "e"]])
            res[0] += v[0]
            res[1] += v[1]
            res[2] = "we" if v[2] == "e" else "wi"
        else:
            # fu => fa, fi, fe, fo
            v = random.choice(
                [["ぁ", "ァ", "a"], ["ぃ", "ィ", "i"], ["ぇ", "ェ", "e"], ["ぉ", "ォ", "o"]]
            )
            res[0] += v[0]
            res[1] += v[1]
            res[2] = res[2][0] + v[2]  # fu => fa
    # characters with small tsu attachable
    if (4 < idx < 25 or 42 < idx) and random.random() < 0.15:
        res[0] = "っ" + res[0]
        res[1] = "ッ" + res[1]
        res[2] = res[2][0] + res[2]  # ka => kka
    # any characters except n, to lengthen its vowel
    if idx != 42 and random.random() < 0.15:
        if res[2][-1] == "a":
            res[0] += "あ"
        elif res[2][-1] == "i":
            res[0] += "い"
        elif res[2][-1] == "u":
            res[0] += "う"
        elif res[2][-1] == "e":
            res[0] += "え"
        elif res[2][-1] == "o":
            res[0] += "お"
        else:
            res[0] += "ー"
        res[1] += "ー"
        res[2] += res[2][-1]
    return res


if __name__ == "__main__":
    while True:
        print(random_kana())
