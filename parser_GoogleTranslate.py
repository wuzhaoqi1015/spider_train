# -*- codeing = utf-8 -*-
# @Author : Wuzhaoqi
# @Software : PyCharm
"""
Google translate API: https://translate.google.cn/translate_a/single?
key: how to clculate the tk?
"""

import js2py
import requests
from faker import Faker


class google_translate(object):
    def __init__(self):
        self.faker = Faker()
        self.url = 'https://translate.google.cn/translate_a/single?client=t&sl=auto&tl={}&hl=zh-CN' \
                   '&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&tk={}&q={}'
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
    def isChinese(text):
        for w in text:
            if '\u4e00' <= w <= '\u9fa5':
                return True
        return False

    def getTk(self, text):
        evaljs = js2py.EvalJs()
        js_code = self.gg_js_code
        evaljs.execute(js_code)
        tk = evaljs.TL(text)
        return tk

    def translate(self, text):
        headers = {
            'User-Agent': self.faker.user_agent(),
        }
        if len(text) > 4891:
            raise RuntimeError('The length of word should be less than 4891...')
        languages = ['zh-CN', 'en']
        if not self.isChinese(text):
            target_language = languages[0]
        else:
            target_language = languages[1]
        res = requests.get(self.url.format(target_language, self.getTk(text), text), headers=headers)
        print(res.json()[0][0][0])
        return [res.json()[0][0][0]]


if __name__ == "__main__":
    word = input("请输入需要翻译的单词:")
    t = google_translate()
    t.translate(word)
