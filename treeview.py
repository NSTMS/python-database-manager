import pandas as pd
import matplotlib.pyplot as plt
import math
import datetime
# Utworzenie listy z danymi o ilości wody potrzebnej na poszczególne drzewa
water_usage = {'sosna': 2, 'brzoza': 1.5, 'tui': 2.2, 'dąb': 1}

# Utworzenie DataFrame z danymi o liczbie poszczególnych drzew
trees = pd.DataFrame({'sosna': [25], 'brzoza': [15], 'tui': [50], 'dąb': [10]})

# Obliczenie całkowitej liczby drzew
total_trees = trees.sum().sum()

# Inicjalizacja wartości początkowej zbiornika wodnego
tank_capacity = 1000

# Utworzenie listy do przechowywania codziennej liczby zużytych litrów wody
daily_water_usage = []

# Przeprowadzenie symulacji od 1 marca 2020 r. do 30 września 2020 r.
current_date = pd.to_datetime('2020-03-01')
end_date = pd.to_datetime('2020-09-30')
while current_date <= end_date:

    # Dodanie wody w soboty
    if current_date.weekday() == 5:
        tank_capacity = 1000

    # Wyliczenie całkowitej liczby zużytych litrów wody w ciągu dnia
    daily_usage = 0
    for tree, usage in water_usage.items():
        daily_usage += trees[tree].iloc[0] * usage
    daily_water_usage.append(daily_usage)

    # Ubytek wody ze zbiornika
    tank_capacity = math.floor(tank_capacity - daily_usage + (0.99 * tank_capacity))

    # Dolewanie wody, jeśli jest jej za mało
    if tank_capacity < 0:
        tank_capacity += 200

    current_date += pd.Timedelta(days=1)

# Obliczenie łącznej ilości wody wyparowanej
total_evaporation = 1000 - tank_capacity

# Wyświetlenie wyników
print('Zadanie 16.1')
print(f'Łączna ilość wyparowanej wody: {abs(total_evaporation)} litrów')

print('Zadanie 16.2')
num_refills = sum([1 for usage in daily_water_usage if usage > tank_capacity])
print(f'Liczba uzupełnień zbiornika: {num_refills}')

print('Zadanie 16.3')
max_pines = math.floor(tank_capacity / water_usage['sosna'])
print(f'Maksymalna liczba sosen, które można posadzić: {max_pines}')

print('Zadanie 16.4')


# dane
x = [datetime.date(2020, 3, 1) + datetime.timedelta(days=i) for i in range(214)]
y = [1000] * 214

sosny = 25
brzozy = 15
tui = 50
duby = 10

woda_sosna = 2
woda_brzoza = 1.5
woda_tuja = 2.2
woda_dab = 1

woda_zbiornik = 1000
woda_dolewanie = 200

# obliczenia
woda_podlewanie = sosny * woda_sosna + brzozy * woda_brzoza + tui * woda_tuja + duby * woda_dab
dni = (datetime.date(2020, 9, 30) - datetime.date(2020, 3, 1)).days

for i in range(dni):
    if i % 7 == 6:  # sobota
        woda_zbiornik += 1000
    woda_zbiornik -= woda_podlewanie
    woda_zbiornik = int(woda_zbiornik * 0.99)
    if woda_zbiornik < woda_podlewanie:
        woda_zbiornik += woda_dolewanie
    y[i] = woda_zbiornik

# wykres
plt.plot(x, y)
plt.title('Stan wody w zbiorniku')
plt.xlabel('Data')
plt.ylabel('Stan wody [l]')
plt.show()

plt.xlabel
