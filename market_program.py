import random
from collections import deque
from g4f.client import Client

class produkty():
    def __init__(self, name , cost, kol):
        self.name = name 
        self.cost = cost
        self.kol = kol 

milk = produkty("молоко",300,1)
cheese = produkty("сыр",500,1)
lamb = produkty("говядина", 2200, 1)
potatoe = produkty("картошка",100,1)
banana = produkty("банан",350,1)

categories = {}
categories["молочном"]=[milk.name,cheese.name]
categories["мясном"]=[lamb.name]
categories["фруктово овощном"]=[potatoe.name,banana.name]
categories[milk.name]=[lamb.name]
categories[cheese.name]=[lamb.name]
categories[lamb.name]=[milk.name,cheese.name,potatoe.name,banana.name]
categories[potatoe.name]=[lamb.name]
categories[banana.name]=[lamb.name]

perevod={milk.name:milk,cheese.name:cheese,lamb.name:lamb,potatoe.name:potatoe,banana.name:banana}
itog={}
frase=["Затем","После чего","После этого","В сторону"]

def razgovor():
    respons=input("Задаите мне любой вопрос и я отвечу")
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": respons}],
        )
    print(response.choices[0].message.content)
    Hello()


def marshrut(checked,search_produkt,position):
    if (search_produkt=="молоко" or search_produkt=="сыр") and position=="молочный":
        print("Вы уже там где нужно")
    elif search_produkt=="говядина" and position=="мясной":
        print("Вы уже там где нужно")
    elif (search_produkt=="банан" or search_produkt=="картошка") and position=="фруктово овощной":
        print("Вы уже там где нужно")
    else:
        print( "Вам сперва в ",checked[0])
        for i in range(len(checked)-1):
            random_int=random.randint(1,3)
            print(frase[random_int],checked[i+1])


def poisk():
    search_produkt=input("Какой товар найти?")
    if search_produkt in perevod:
        position=input("В каком вы отделе?").lower()
        if position in categories:
            search_q=deque()##Создание очереди
            search_q += categories[position]
            checked=[]
            while search_q:
                person = search_q.popleft()
                if person not in checked:
                    if search_produkt==person:
                        print("мы нашли ваш товар.")
                        marshrut(checked,search_produkt,position)
                        question_buy=input("Вы хотите его купить?")
                        if question_buy.lower() == "да":
                            Add_to_korzina(person)
                            break
                        else:
                            print("Хорошо.")
                            Hello()
                    else:
                        search_q+=categories[person]
                        checked.append(person)
        else:
                    print("У нас нет такого отдела или я вас не правильно понял , пожалуйста повторите.")
                    poisk()
    else:
        print("К большому сожалению такого товара у нас в магазине нет(")
        Hello()
    

def Add_to_korzina(person):
    global itog
    kol_of_produkt=int(input("Сколько товара вы хотите взять?"))#количество покупаемого продукта
    if kol_of_produkt == 0:
        print("Вы не можете взять 0.")
        Add_to_korzina(person)
    else:
        cost_of_produkt= kol_of_produkt * perevod[person].cost #нахождение цены продукта в корзине
        itog[person] = cost_of_produkt  #добавление продукта в корзину
        print("Ваш товар был успешно добавлен в корзину.")
    Hello()
        
def korzina_see():
    arr_cost=list(itog.values())
    arr_produkts=list(itog.keys())
    total_cost = 0 
    print("Продукт      Кол-во      Цена")
    for i in arr_produkts:
        perevedeno=perevod[i]
        cost_produkt=perevedeno.kol*perevedeno.cost
        print(i," x",perevedeno.kol," ",cost_produkt,"тг")
    for i in arr_cost:
        total_cost+=i
    print("Ваша общая цена корзины-",total_cost)
    Hello()

def oplata():
    arr_cost=list(itog.values())
    total_cost = 0 
    for i in arr_cost:
        total_cost+=i
    HDYWTP=input("Как вы хотите заплатить?")
    if HDYWTP.lower()=="картой":
        WB=input("Какого банка?")
        print("С вас ",total_cost, "можете подставить к терминулу.")
    elif HDYWTP.lower()=="наличными":
        print("Хорошо , даваите их сюда.")
    else:
        print("Я вас не расслышал,пожалуйста повторите.")
        oplata()
    print("До свидания!")

def Hello():
    start=input("Чем я могу вам помочь?")
    if start.lower()=="найти продукт":
        poisk()
    elif start.lower()=="посмотреть корзину":
        korzina_see()
    elif start.lower()=="оплата":
        oplata()
    elif start.lower()=="давай поговорим":
        razgovor()
    else:
        print("Я вас не расслышал")
        Hello()

print("Добро пожаловать в наш магазин!")
Hello()
