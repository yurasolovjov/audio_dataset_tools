# audio_dataset_tools
Данный программный модуль предназначен для разработки звуковых датасетов c использованием источников:
  - [Audioset][df1]
  - [Youtube8M][df2]
  - [Urbansound][df3]
  - [Freesound.org][df4]

Примеры запуска утилиты:

```python
#Запуск утилиты на анализ датасета Audioset
python main.py --tools audioset --analysis True -d eval_segments.csv

#Запуск утилиты на cкачивание датасета Audioset
python main.py --tools audioset -d eval_segments.csv --out audioset_download

#Запуск утилиты на анализ запрашиваемых данных из freesound.org
python main.py --tools freesound -a True --gen_key_freesound key --search door --search glass --search speech --lim_page 2

#Запуск утилиты на скачивание запрашиваемых данных из freesound.org
python main.py --tools freesound -a True --gen_key_freesound key --search door --search glass --search speech --lim_page 2


```



[df1]: <https://research.google.com/audioset/>
[df2]: <https://research.google.com/youtube8m/>
[df3]: <https://urbansounddataset.weebly.com/>
[df4]: <https://freesound.org/>

