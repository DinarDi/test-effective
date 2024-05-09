import datetime
import json


class FinanceNote:
    notes: list[dict] | None = None
    balance: float

    def __init__(self, filename: str):
        self.filename: str = filename
        self.load_data()

    def load_data(self):
        """Загрузка данных из json файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.notes = data['notes']
                self.balance = data['balance']
        except (FileNotFoundError, json.JSONDecodeError):
            self.notes = []
            self.balance = 0.0

    def save_data(self):
        """Сохранение данных в json файл"""
        data = {
            'notes': self.notes,
            'balance': self.balance
        }
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def validate_inputs(
            self,
            date: str | None = None,
            category: str | None = None,
            num: str | None = None,
    ):
        """
        Проверка введенных пользователем данных
        :param date: Дата
        :param category: Категория
        :param num: Число
        :return: list | None
        """
        errors = []
        if date or date == '':
            # Проверка даты
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                errors.append('Введен неверный формат даты. Пожалуйста, введите дату в формате (YYYY-MM-DD)')
        if category or category == '':
            # Проверка категории
            if category not in ('доход', 'расход'):
                errors.append('Введена неверная категория. Пожалуйста, введите правильную категорию (доход/расход)')
        if num or num == '':
            # Проверка суммы
            try:
                amount = float(num)
                if amount < 0:
                    errors.append('Сумма должна быть больше 0. Пожалуйста, введите корректную сумму')
            except ValueError:
                errors.append('Неверный формат суммы. Пожалуйста, введите число')

        if errors:
            return errors
        else:
            return None

    def get_balance(self):
        print(f'----Ваш баланс равен: {self.balance}----')

    def add_note(self):
        """Добавление новой записи"""
        while True:
            # Ввод даты
            date = input('Введите дату в формате (YYYY-MM-DD): ')
            errors = self.validate_inputs(date=date)
            if not errors:
                break
            else:
                print('\n'.join(errors))
        while True:
            # Ввод категории
            category = input('Введите категорию (доход/расход): ')
            errors = self.validate_inputs(category=category)
            if not errors:
                break
            else:
                print('\n'.join(errors))
        while True:
            # Ввод суммы
            amount = input('Введите сумму: ')
            errors = self.validate_inputs(num=amount)
            if not errors:
                amount = float(amount)
                break
            else:
                print('\n'.join(errors))
        description = input('Введите описание: ')
        note = {
            'id': len(self.notes) + 1,
            'date': date,
            'category': category,
            'amount': amount,
            'description': description,
        }
        self.notes.append(note)
        if category == 'доход':
            self.balance += amount
        else:
            self.balance -= amount
        self.save_data()
        print('----Запись добавлена----')

    def edit_note(self):
        """Редактирование записи"""
        if not self.notes:
            print('----Нет записей для редактирования----')
            return
        for note in self.notes:
            print(
                f"{note['id']}. {note['date']} - {note['category']}: {note['amount']} {note['description']}"
            )
        while True:
            note_id = input('Введите id записи, которую хотите изменить или введите 0 для выхода в меню: ')
            errors = self.validate_inputs(num=note_id)
            if not errors:
                note_id = int(note_id)
                break
            else:
                print('\n'.join(errors))

        if 1 <= note_id <= len(self.notes):
            note = self.notes[note_id - 1]
            while True:
                # Ввод новой даты
                new_date = input('Введите новую дату или оставьте поле пустым: ')
                if new_date == '':
                    new_date = note['date']
                    break
                else:
                    errors = self.validate_inputs(date=new_date)
                    if not errors:
                        break
                    else:
                        print('\n'.join(errors))

            while True:
                # Ввод новой категории
                new_category = input('Введите новую категорию или оставьте поле пустым: ')
                if new_category == '':
                    new_category = note['category']
                    break
                else:
                    errors = self.validate_inputs(category=new_category)
                    if not errors:
                        break
                    else:
                        print('\n'.join(errors))

            while True:
                # Ввод новой суммы
                new_amount = input('Введите новую сумму или оставьте поле пустым: ')
                if new_amount == '':
                    new_amount = note['amount']
                    break
                else:
                    errors = self.validate_inputs(num=new_amount)
                    if not errors:
                        new_amount = float(new_amount)
                        break
                    else:
                        print('\n'.join(errors))
            new_description = input('Введите новое описание или оставьте поле пустым: ') or note['description']

            old_amount = note['amount']
            old_category = note['category']

            note['date'] = new_date
            note['category'] = new_category
            note['amount'] = new_amount
            note['description'] = new_description

            if new_category == 'доход' and old_category == 'доход':
                self.balance -= old_amount
                self.balance += new_amount
            elif new_category == 'доход' and old_category == 'расход':
                self.balance += old_amount + new_amount
            elif new_category == 'расход' and old_category == 'доход':
                self.balance -= old_amount
                self.balance -= new_amount
            else:
                self.balance += old_amount
                self.balance -= new_amount
            self.save_data()
            print('----Запись изменена----')
        if note_id == 0:
            return

    def search_notes(self):
        """Поиск записей"""
        if not self.notes:
            print('----Нет записей для поиска----')
            return
        while True:
            # Ввод по какому полю будет производиться поиск
            search_param = input('Введите по какому полю производится поиск (дата, категория, сумма): ')
            if search_param in ('дата', 'категория', 'сумма'):
                break
            else:
                print('Неверный ввод. Введите по какому полю производится поиск (дата, категория, сумма): ')

        while True:
            # Ввод запроса поиска
            search_request = input('Введите запрос поиска: ')
            if search_param == 'дата':
                errors = self.validate_inputs(date=search_request)
                if not errors:
                    break
                else:
                    print('\n'.join(errors))
            elif search_param == 'категория':
                errors = self.validate_inputs(category=search_request)
                if not errors:
                    break
                else:
                    print('\n'.join(errors))
            else:
                errors = self.validate_inputs(num=search_request)
                if not errors:
                    break
                else:
                    print('\n'.join(errors))

        # Поиск записей
        founded_notes = []
        if search_param in ('дата', 'категория'):
            for note in self.notes:
                if search_request in note['date'] or \
                        search_request in note['category']:
                    founded_notes.append(note)
        else:
            for note in self.notes:
                if float(search_request) == note['amount']:
                    founded_notes.append(note)
        if founded_notes:
            for note in founded_notes:
                print(
                    f"{note['id']}. {note['date']} - {note['category']}: {note['amount']} {note['description']}"
                )
        else:
            print('----Ничего не найдено----')

    def menu(self):
        """Отображение меню приложения"""
        print('----MENU----')
        print('1. Вывод баланса')
        print('2. Добавить запись')
        print('3. Редактировать запись')
        print('4. Поиск по записям')
        print('0. Выход')


if __name__ == '__main__':
    finance = FinanceNote(filename='wallet.json')
    while True:
        finance.menu()
        while True:
            # Проверка ввел ли пользователь число
            choice = input('Введите число нужной операции: ')
            errors = finance.validate_inputs(num=choice)
            if not errors:
                choice = int(choice)
                break
            else:
                print('\n'.join(errors))

        match choice:
            case 1:
                finance.get_balance()
            case 2:
                finance.add_note()
            case 3:
                finance.edit_note()
            case 4:
                finance.search_notes()
            case 0:
                print('----Выход из приложения----')
                break
            case _:
                print('Неверный ввод. Пожалуйста, введите правильную операцию.')
