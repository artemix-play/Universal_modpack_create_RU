import moremods
import default

try:
    print('Выберите режим:\n1.Обычный режим\n2.Многомодовый режим')
    in_user = int(input('> '))
    if in_user == 1:
        mod_name = input('Введите название мода: ')
        default.start(mod_name)
    elif in_user == 2:
        coreverison = input('Введите версию и ядро (например: 1.20.1 Forge): ')
        mod_names = input('Введите названия модов через запятую (например Create,Mekanism): ')
        mod_names = mod_names.split(',')
        moremods.start(mod_names, coreverison)
    else:
        print('Ошибка радиуса')
        exit()

except Exception as e:
        print(f"Ошибка: {e}")
        exit()