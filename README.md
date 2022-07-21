# Вычисление добротности и ее случайной погрешности с помощью автоматического векторного сетевого анализатора

## Описание

Программа помогает вычислять добротность и её случайную погрешность в электрической цепи по измерениям векторного анализатора.

Программа принимает на вход файл с измерениями сетевого анализатора в формате .snp или csv.
По этому файлу вычисляется добротность нагруженного (Q_l) и ненагруженного (Q_0) резонатора.
Для этих величин также вычисляется случайная погрешность.
Кроме того строится диаграмма Смита и график зависимости модуля коэффициента отражения от частоты.

Диаграмма Смита представляет собой математическое преобразование двумерной декартовой комплексной плоскости.
Она помогает удобно представить поведение резонатора при изменении частоты сигнала.

Интерфейс программы:

![Program interface1](./resource/repository/readme_img1.png?raw=true)
![Program interface2](./resource/repository/readme_img2.png?raw=true)

Запуск:
streamlit run source/main.py

## Usage

App calculates the quality factor and its random error in the electric circuit
for the set of [vector analyzer](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) measuremets.

How to start:
streamlit run source/main.py

## Input data

The measurements made by a vector network analyzer (set of frequencies and corresponding network parameters).
Main supported file format is .snp, but similar formats are accepted too. Noise data is not supported.

* Supported network parameters: reflection coefficient (S), impedance (Z)
* Supported parameters representations:
real and imaginary; magnitude and angle; db and angle

## Result

* Loaded and unloaded quality factor (q-factor) with random errors
* plot amplitude vs frequency
* [Smith chart](https://en.wikipedia.org/wiki/Smith_chart)