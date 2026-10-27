from django.core.management.base import BaseCommand
from main.models import Product

class Command(BaseCommand):
    help = 'Автоматически заполняет базу данных меню Runy Coffee'

    def handle(self, *args, **kwargs):
        menu_data = [
            # КОФЕ (category='coffee')
            {"name": "Эспрессо", "desc": "кофе, вода", "price": 150, "cat": "coffee"},
            {"name": "Американо", "desc": "эспрессо, горячая вода", "price": 180, "cat": "coffee"},
            {"name": "Капучино", "desc": "эспрессо, молоко, молочная пенка", "price": 220, "cat": "coffee"},
            {"name": "Латте", "desc": "эспрессо, молоко", "price": 240, "cat": "coffee"},
            {"name": "Флэт уайт", "desc": "двойной эспрессо, молоко", "price": 250, "cat": "coffee"},
            {"name": "Мокка", "desc": "эспрессо, молоко, шоколадный сироп", "price": 260, "cat": "coffee"},
            {"name": "Раф", "desc": "эспрессо, сливки, молоко, сахар, ваниль", "price": 270, "cat": "coffee"},

            # ЧАЙ И ДРУГИЕ НАПИТКИ (category='drink')
            {"name": "Чёрный чай", "desc": "чёрный чай, вода", "price": 150, "cat": "drink"},
            {"name": "Зелёный чай", "desc": "зелёный чай, вода", "price": 150, "cat": "drink"},
            {"name": "Травяной чай", "desc": "травяной сбор, вода", "price": 180, "cat": "drink"},
            {"name": "Какао", "desc": "какао-порошок, молоко, сахар", "price": 200, "cat": "drink"},
            {"name": "Горячий шоколад", "desc": "шоколад, молоко", "price": 220, "cat": "drink"},
            {"name": "Лимонад домашний", "desc": "лимон, вода, сахар, мята", "price": 190, "cat": "drink"},
            {"name": "Сок апельсиновый", "desc": "апельсин", "price": 150, "cat": "drink"},
            {"name": "Сок яблочный", "desc": "яблоко", "price": 150, "cat": "drink"},
            {"name": "Вода питьевая", "desc": "вода", "price": 80, "cat": "drink"},

            # ВЫПЕЧКА (category='food')
            {"name": "Круассан классический", "desc": "пшеничная мука, сливочное масло, дрожжи, молоко, сахар, соль", "price": 180, "cat": "food"},
            {"name": "Круассан с миндалём", "desc": "пшеничная мука, сливочное масло, дрожжи, молоко, сахар, соль, миндаль, миндальный крем", "price": 220, "cat": "food"},
            {"name": "Маффин шоколадный", "desc": "мука, яйца, сахар, какао, шоколад, сливочное масло, разрыхлитель", "price": 160, "cat": "food"},
            {"name": "Синнабон", "desc": "мука, молоко, дрожжи, сахар, корица, сливочное масло, сливочный сыр", "price": 200, "cat": "food"},
            {"name": "Печенье овсяное", "desc": "овсяные хлопья, мука, сахар, сливочное масло, яйца", "price": 90, "cat": "food"},

            # ЗАВТРАКИ (category='food')
            {"name": "Сырники со сметаной", "desc": "творог, яйца, мука, сахар, сметана", "price": 280, "cat": "food"},
            {"name": "Омлет с сыром и зеленью", "desc": "яйца, молоко, сыр, зелень, масло", "price": 260, "cat": "food"},
            {"name": "Каша овсяная с ягодами", "desc": "овсяные хлопья, молоко, ягоды, сахар", "price": 240, "cat": "food"},
            {"name": "Тост с авокадо и яйцом", "desc": "хлеб, авокадо, яйцо, соль, перец, зелень", "price": 320, "cat": "food"},

            # ДЕСЕРТЫ (category='food')
            {"name": "Чизкейк Нью-Йорк", "desc": "сливочный сыр, печенье, сливочное масло, сахар, яйца, сливки", "price": 280, "cat": "food"},
            {"name": "Тирамису", "desc": "маскарпоне, печенье савоярди, кофе, какао, яйца, сахар", "price": 300, "cat": "food"},
            {"name": "Брауни", "desc": "шоколад, сливочное масло, сахар, яйца, мука, какао", "price": 220, "cat": "food"},
            {"name": "Мороженое (1 шарик)", "desc": "молоко, сливки, сахар, ваниль", "price": 120, "cat": "food"},
        ]

        self.stdout.write("Начинаю загрузку меню...")
        count = 0

        for item in menu_data:
            # get_or_create создаст блюдо, если его нет, и не создаст дубликат, если запустить скрипт дважды
            obj, created = Product.objects.get_or_create(
                name=item["name"],
                defaults={
                    "description": item["desc"],
                    "price": item["price"],
                    "category": item["cat"],
                }
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Успешно добавлено новых позиций: {count}"))
