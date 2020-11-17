# -*- codeing = utf-8 -*-
# @Author : Wuzhaoqi
# @Software : PyCharm

import js2py
import requests
from faker import Faker


class GoogleTranslate(object):
    """
    Google translate API: https://translate.google.cn/translate_a/single?
    How to calculate the value 'tk'?: self.get_tk
    How to determine if it is Chinese: self.is_chinese
    How to translate：self.translate: self.translate
    """
    def __init__(self):
        self.faker = Faker()
        self.url = 'https://translate.google.cn/translate_a/single?client=t&sl={}&tl={}&hl=zh-CN' \
                   '&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&tk={}&q={}'
        self.headers = {
            'User-Agent': self.faker.user_agent(),
        }
        self.languages = ['zh-CN', 'zh-TW', 'en', 'fr', 'de', 'ja', 'ko', 'ru', 'es']
        """
        zh-CN: 中文简体
        zh-TW：中文繁体
        en: 英语
        fr: 法语
        de: 德语
        ja: 日语
        ko: 韩语
        ru: 俄语
        es: 西班牙语
        """
        self.gg_js_code = '''
                function TL(a) {
                    var k = "";
                    var b = 406644;
                    var b1 = 3293161072;
                    var jd = ".";
                    var $b = "+-a^+6";
                    var Zb = "+-3^+b+-f";
                    for (var e = [], f = 0, g = 0; g < a.length; g++) {
                        var m = a.charCodeAt(g);
                        128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < 
                        a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) +
                         (a.charCodeAt(++g) & 1023),
                        e[f++] = m >> 18 | 240,
                        e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                        e[f++] = m >> 6 & 63 | 128),
                        e[f++] = m & 63 | 128)
                    }
                    a = b;
                    for (f = 0; f < e.length; f++) a += e[f],
                    a = RL(a, $b);
                    a = RL(a, Zb);
                    a ^= b1 || 0;
                    0 > a && (a = (a & 2147483647) + 2147483648);
                    a %= 1E6;
                    return a.toString() + jd + (a ^ b)
                };
                function RL(a, b) {
                    var t = "a";
                    var Yb = "+";
                    for (var c = 0; c < b.length - 2; c += 3) {
                        var d = b.charAt(c + 2),
                        d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                        d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
                    }
                    return a
                }
            '''

    @staticmethod
    def is_chinese(text):
        for w in text:
            if '\u4e00' <= w <= '\u9fa5':
                return True
        return False

    def get_tk(self, text):
        evaljs = js2py.EvalJs()
        js_code = self.gg_js_code
        evaljs.execute(js_code)
        tk = evaljs.TL(text)
        return tk

    def translate(self, text, tl=None, sl='auto'):
        """
        :param text: the text you want to translate
        :param tl: the target language
        :param sl: the source language
        :return: the text was transalated
        """
        if len(text) > 4891:
            raise RuntimeError('The length of text should be less than 4891...')
        if tl is None:
            if not self.is_chinese(text):
                target_language = self.languages[0]
            else:
                target_language = self.languages[1]
        else:
            if tl not in self.languages:
                raise ValueError("the language must be{}".format(self.languages))
            target_language = tl
        res = requests.get(self.url.format(sl, target_language, self.get_tk(text), text), headers=self.headers)
        return res.json()[0][0][0]


if __name__ == "__main__":
    t = GoogleTranslate()
    text_en = 'The quick brown fox jumped over the lazy dog'
    text_ja = t.translate(text_en, tl='ja')
    text_de = t.translate(text_ja, tl='de')
    text_fr = t.translate(text_de, tl='fr')
    text_en_new = t.translate(text_fr, tl='en')
