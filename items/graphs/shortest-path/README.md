## Поиск кратчайшего пути в графе с GUI

### Описание

Приложение позволяет визуализировать граф и выполнять поиск кратчайшего пути в нем.
Для поиска доступны следующие алгоритмы: 
- Алгоритм Беллмана-Форда

Программа выдает два типа графа: исходный и граф и граф кратчайшего пути.


### Интерфейс

![image](https://github.com/JKearnsl/short_path_in_graph/assets/76239707/d99327da-2fed-4089-b56e-b84586bd3aa3)

![image](https://github.com/JKearnsl/short_path_in_graph/assets/76239707/072db912-e595-4041-810d-d4a5cbbf3b8a)


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
