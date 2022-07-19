from termcolor import cprint
from random import randint

# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:
    money = 100
    food = 50
    dirt = 0
    eaten = 0
    felix = 30

    def __init__(self):
        pass

    def __str__(self):
        return 'В доме осталось денег {}, еды {}, грязи {}'.format(
            self.money, self.food, self.dirt)


class Husband:
    fullness = 30
    happiness = 100
    annual_income = 0

    def __init__(self, name):
        self.name = name

    def __str__(self):
        # return super().__str__()
        return '{}, сытость {}, счастье {}'.format(
            self.name, self.fullness, self.happiness)

    def act(self):
        House.dirt += 5
        if self.fullness < 0:
            cprint('{} - смерть от голода'.format(self.name), color='red')
        elif self.happiness < 10:
            cprint('{} - смерть от депресии'.format(self.name), color='red')
        elif House.dirt > 90:
            self.happiness -= 10
        # dice = randint(1, 5)
        if self.fullness <= 30:
            self.eat()
        elif House.money < 300:
            self.work()
        else:
            self.gaming()

    def eat(self):
        self.fullness += 30
        House.food -= 30
        House.eaten += 30
        print('{} после обеда - сытость {}'.format(self.name, self.fullness))

    def work(self):
        self.fullness -= 10
        House.money += 150
        self.annual_income += randint(50, 400)
        print('{} сходил на работу, денег +150'.format(self.name))

    def gaming(self):
        self.fullness -= 10
        self.happiness += 20
        print('{} играл в танки весь день, сытость -10, счастье +20'.format(self.name))


class Wife:
    fullness = 30
    happiness = 100
    total_fur_coats = 0

    def __init__(self, name):
        self.name = name

    def __str__(self):
        # return super().__str__()
        return '{}, сытость {}, счастье {}'.format(
            self.name, self.fullness, self.happiness)

    def act(self):
        if self.fullness < 0:
            cprint('{} - смерть от голода'.format(self.name), color='red')
        elif self.happiness < 10:
            cprint('{} - смерть от депресии'.format(self.name), color='red')
        elif House.dirt > 90:
            self.happiness -= 10
        dice = randint(1, 6)
        if self.fullness <= 20:
            self.eat()
        elif House.food <= 60:
            self.shopping()
        elif dice == 1:
            self.clean_house()
        elif dice == 2:
            self.buy_fur_coat()
        else:
            pass

    def eat(self):
        self.fullness += 30
        House.food -= 30
        House.eaten += 30
        print('{} после обеда: сытость {}'.format(self.name, self.fullness))

    def shopping(self):
        if House.money >= 100:
            self.fullness -= 10
            House.food += 100
            House.money -= 100
            print('{} сходила в магазин, продуктов +100'.format(self.name))
        else:
            cprint('Деньги кончились', color='red')

    def buy_fur_coat(self):
        if House.money >= 350:
            self.total_fur_coats += 1
            self.fullness -= 10
            House.money -= 350
            self.happiness += 20
            print('{} купила шубу, счастье +{}'.format(self.name, self.happiness))
        else:
            self.happiness -= 1
            cprint('{} хочет новую шубу '.format(self.name), color='red')

    def clean_house(self):
        House.dirt -= 100
        self.fullness -= 10
        print('{} убрала дом, грязи {}, сытость {}'.format(self.name, House.dirt, self.fullness))


home = House()
serge = Husband(name='Сережа')
masha = Wife(name='Маша')

for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    serge.act()
    masha.act()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(home, color='cyan')

print('Всего заработано денег {}, сьедено еды {}, куплено шуб {}'.format(
    serge.annual_income, House.eaten, masha.total_fur_coats))
