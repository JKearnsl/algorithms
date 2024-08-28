## Поиск кратчайшего пути в графе с GUI

### Описание

Приложение позволяет визуализировать граф и выполнять поиск кратчайшего пути в нем.
Для поиска доступны следующие алгоритмы: 
- Алгоритм Беллмана-Форда

Программа выдает два типа графа: исходный и граф и граф кратчайшего пути.


### Интерфейс

![image](https://github.com/user-attachments/assets/a52c75b9-dbd7-42f4-a307-cacdd8b7a4cd)

![image](https://github.com/user-attachments/assets/20980125-a809-4759-8cf2-ab57f225f3da)



### Алгоритм Беллмана-Форда

https://github.com/JKearnsl/short_path_in_graph/blob/ad6ad59df5afcddd360a79b653d93cf7a3044a83/src/model/fsp/bfa.py#L4-L38

### Сборка

Приложение написано на `Python3.11`. Необходимо установить следующие библиотеки:

- `PyQt6`
- `networkx`
- `matplotlib`

Для запуска приложения необходимо выполнить команду `python3 main.pyw` в корневой директории проекта. 
Не забудьте добавить в `PYTHONPATH` путь к директории с Вашим проектом,
например: `export PYTHONPATH="/home/jkearnsl/Рабочий стол/project1"`.
