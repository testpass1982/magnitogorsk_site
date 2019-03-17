import re

text = 'test 123 text bool lorem, five text test, /img/social__icon-01.png , /img/social__icon-02.png, /img/social__icon-03.png \
    /img/back__arrow-01.png test 123 text bool lorem, five text test'

pattern = re.compile('([\/-]\S*\.[jpg|png|gif]{3})')
for pat in pattern.findall(text):
    mod_pattern =  f"{{% static '{pat[1:]}' %}}"
    new_text = re.sub(pattern, mod_pattern, text)

print(new_text)