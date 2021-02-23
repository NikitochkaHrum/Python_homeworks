import pickle
import sklearn
import pandas as pd
import argparse

path_of_model = "detecting_anime_lovers"

with open(path_of_model, 'rb') as f:
    model = pickle.load(f)
parser = argparse.ArgumentParser()
parser.add_argument("datan")
parser.add_argument("result")

args = parser.parse_args()
print(args)
data = pd.read_csv(args.datan)

# чистим долго
data.rename(columns={'Отметка времени':'time', 'Мальчик или девочка?':'sex', 'Как часто тебя били в детстве?':'child_offence'}, inplace=True)
data.rename(columns={'Оцените ваш уровень вегетарианца по 5-ти бальной шкале':'vegan', 'Что такое два.ч?':'dvach', 'Твоя ориентация?':'gender'}, inplace=True)
data.rename(columns={'Погулять вечером после тяжкого рабочего дня, или посычевать дома?':'rest', 'Как часто играешь в игры?':'games'}, inplace=True)
data.rename(columns={'Сериалы?':'series', 'А книги? ':'books', 'Вы таки антисемит? ':'antisemetism'}, inplace=True)
data.rename(columns={'Какой предмет ближе всего по душе?':'subject', 'Как вы относитесь к аннексии Крыма?':'crimea', 'Владимир Путин - ':'putin'}, inplace=True)
data.rename(columns={'Как хорошо вы знаете английский?':'english', 'Было ли раньше лучше? ':'USSR_lover'}, inplace=True)
if "А какие жанры фильмов любишь? " in data.columns:
    data.drop(["А какие жанры фильмов любишь? "], axis=1, inplace=True)
data.loc[data.sex == 'Мальчик', ['sex']] = 0
data.loc[data.sex == 'Девочка', ['sex']] = 1
data.sex = data.sex.astype('int8')
data.loc[data.rest == 'Гулять', ['rest']] = 0
data.loc[data.rest == 'Сычевать', ['rest']] = 1
data.rest=data.rest.astype('int8')
data.loc[data.english == 'Оригатоё гайзаймас', ['english']] = 0
data.loc[data.english == 'Чуть лучше, чем ничего', ['english']] = 1
data.loc[data.english == 'Нормально', ['english']] = 2
data.loc[data.english == 'Хорошо', ['english']] = 3
data.loc[data.english == 'Отлично', ['english']] = 4
data.loc[data.english == 'НЭЙТИВ ИНГЛИШ СПИКЕР', ['english']] = 5
data.english = data.english.astype('int8')
data = data.join(pd.get_dummies(data.child_offence, prefix='child_offence'))
data = data.join(pd.get_dummies(data.dvach, prefix='dvach'))
data = data.join(pd.get_dummies(data.gender, prefix='gender'))
data = data.join(pd.get_dummies(data.antisemetism, prefix='antisemetism'))
data = data.join(pd.get_dummies(data.subject, prefix='subject'))
data = data.join(pd.get_dummies(data.crimea, prefix='crimea'))
data.drop(['child_offence', 'dvach', 'gender', 'antisemetism', 'subject', 'crimea'], axis=1, inplace=True)
data.loc[data.putin == 'Молодец', ['putin']] = 'putin_good'
data.loc[data.putin == 'Политик, лидер и боец', ['putin']] = 'putin_good'
data.loc[data.putin != 'putin_good', ['putin']] = 'rebel'
data = data.join(pd.get_dummies(data.putin))
data.drop(['putin'], axis=1, inplace=True)
data.loc[data.USSR_lover != 'Нет', ['USSR_lover']] = 1
data.loc[data.USSR_lover == 'Нет', ['USSR_lover']] = 0
data.drop(["time"], axis=1, inplace=True)

ans = model.predict(data)
a = []
for i in range(len(ans)):
    if ans[i]:
        a.append(1)
    else:
        a.append(0)
answer = pd.Series(a, name="res")
answer.to_csv(args.result)
