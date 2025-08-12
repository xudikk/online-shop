# Takrorshlash -> Funksiyalar bn ishlash | default parametrlar,  *args, **kwargs

# funksiya -> kodlar yozilgan qolip

# umumiy sintaksiz!!!
# def nom(param1, param2, .....):    # defination qisqartmasi
#     # qilishini keraak bo'lgan umumiy codelar


# def salom():
#     print("Assalomu Alaykum Eshmatjon")
#     print("Xayr eshmaatjon")
#
#
# salom()
# salom()
# salom()
# salom()
# salom()



# paramert va argumentlar
odam = "Eshmaat"


# def salom(ism: str, yosh=0, hobbilar=[]):  # bu yerda ism-parametr, parametrlar istalgan olishi mumkin!
#     print(ism.upper)
#     print(yosh)
#     hobbilar.sort()
#     print(hobbilar)


# salom("Alijon", hobbilar=['yotish', "uxlash", 'roblox', 'cs2'])   # bular argumentlar!!


# *args  -> arguments(cheksiz argumentlar olish imkonini beradi) (tupleda yig'adi)
# **kwargs  -> keyword arguments (Cheksiz kalitlar orqali argument olish imkonini beradi)(dictda yig'adi)
# Qoida! 1-params | 2 (yoki 3)- *args | 3 (yoki 2)-defaultparams | 4 -  **kwargs
# def salom(ism, nimadir, yosh=5, *args, **kwargs):
#     print(ism, yosh)
#     print(args)
#     print(kwargs)
#
#
# salom("ali", 34, 3456, 678, 234, 987, 345, 765, maosh=500, viloyat='buxoro', kasb='bekorchi')






