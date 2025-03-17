# goit-pythonweb-hw-06


### **Тестування CLI**
Тепер, якщо ви запустите команду:

```bash
python main.py -a list -m Teacher
```

Ви отримаєте вивід, наприклад:

```
📋 Список teachers:
   Teacher(id=1, name='Boris Jonson')
   Teacher(id=2, name='Andry Bezos')
   Teacher(id=3, name='Elon Musk')
```
✅ **Створити вчителя:**
```bash
python main.py -a create -m Teacher -n "Boris Jonson"
```

✅ **Створити групу:**
```bash
python main.py -a create -m Group -n "AD-101"
```

✅ **Список усіх вчителів:**
```bash
python main.py -a list -m Teacher
```

✅ **Оновити ім'я викладача (ID = 3):**
```bash
python main.py -a update -m Teacher --id 3 -n "Andry Bezos"
```

✅ **Видалити викладача (ID = 3):**
```bash
python main.py -a remove -m Teacher --id 3
```

---

