import re
def is_discrediting_the_authorities(text):
    return bool(re.search(r'киев.*(режим|хунта|неонац|наркоман|клоун)|(шаровар|укро|свино|неонац).*(рейх|вермахт)|наркоман.*киев|(наркоман|клоун|упорот|марионетка).*(зеленск|зеля)|государственный переворот', text, flags=re.I))

def is_humiliation_of_culture_narrative(text):
    return bool(re.search(r'укроп|чубат|хохол|хохля|укры|салоед|кастрюл.*голов|кукраин|бандеров|укронацист|укровояк', text, flags=re.I))

def is_external_influence_narrative(text):
    return bool(re.search(r'внешн.*руково|(президент|зелен|наркоман).*марионет|укр.*прихвост|жизнями.*укр', text, flags=re.I))

def is_military_actions_narrative(text):
    return bool(re.search(r'тик-ток.*войска|очеред.*победа|(перемог|побед).*по-украин|воюют с мирним|пушеч.*мясо|расход.*материал|наемыш|неб.*(тысяча|милион)', text, flags=re.I))

def is_betrayal_of_partners_narrative(text):
    return bool(re.search(r'', text, flags=re.I))

def is_internal_conflict_narrative(text):
    return bool(re.search(r'', text, flags=re.I))

def is_historical_dependence_narrative(text):
    return bool(re.search(r'', text, flags=re.I))

def is_war_is_secret_duty_narrative(text):
    return bool(re.search(r'', text, flags=re.I))

def is_illegimate_government_narrative(text):
    return bool(re.search(r'', text, flags=re.I))
