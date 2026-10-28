"""Carga datos de demostración: marcas, perfumes, cupones, clientes y pedidos.

Uso:  python manage.py seed_store          (solo si la base está vacía)
      python manage.py seed_store --reset  (borra catálogo, pedidos y clientes demo)
"""

import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from apps.accounts.models import Profile
from apps.catalog.models import Brand, Category, Coupon, Product, ProductImage
from apps.orders.models import Order, OrderItem, PaymentMethod, ShippingMethod, shipping_cost

User = get_user_model()

CATEGORIES = [
    ("Caballeros", "caballeros", "Amaderados, acuáticos y aromáticos para el día a día y la noche.", "img/editorial/caballeros.webp"),
    ("Damas", "damas", "Florales, gourmand y chipres de las casas que más se regalan.", "img/editorial/damas.webp"),
    ("Niños", "ninos", "Colonias suaves, con poco alcohol y aromas limpios.", "img/editorial/ninos.webp"),
]

BRANDS = [
    ("Chanel", "Francia", True, "Casa parisina fundada por Gabrielle Chanel. Sus perfumes N°5 y Coco Mademoiselle siguen entre los más regalados del mundo."),
    ("Versace", "Italia", True, "Casa de moda italiana con fragancias intensas y de gran proyección."),
    ("Giorgio Armani", "Italia", True, "Fragancias limpias y luminosas; Acqua di Giò es su referencia acuática."),
    ("Dolce & Gabbana", "Italia", True, "Perfumes de inspiración mediterránea, con The One como línea insignia."),
    ("Prada", "Italia", True, "Composiciones modernas, entre lo aromático y lo gourmand."),
    ("Hugo Boss", "Alemania", False, "Fragancias versátiles y fáciles de llevar a la oficina."),
    ("Yves Saint Laurent", "Francia", True, "Casa francesa con perfumes de carácter, como Black Opium."),
    ("Lancôme", "Francia", True, "Belleza francesa; La Vie Est Belle es uno de sus éxitos más duraderos."),
    ("Miu Miu", "Italia", False, "La línea más fresca y juvenil del grupo Prada."),
    ("Guerlain", "Francia", True, "Perfumista histórico de París, con la serie cítrica Aqua Allegoria."),
    ("Narciso Rodriguez", "Estados Unidos", False, "Perfumes construidos alrededor del almizcle, sobrios y envolventes."),
    ("Antonio Banderas", "España", False, "Fragancias accesibles con buena relación precio y duración."),
    ("Escada", "Alemania", False, "Florales y frutales luminosos, ideales para clima cálido."),
    ("Petit Atelier", "Marca de demostración", False, "Línea infantil de demostración: colonias suaves con bajo contenido de alcohol."),
]

# nombre, marca, categoría, familia, concentración, ml, precio, precio anterior, stock, imagen, destacado,
# descripción corta, salida, corazón, fondo, galería
PRODUCTS = [
    ("Bleu de Chanel", "Chanel", "caballeros", "amaderada", "edp", 100, "165.00", None, 14, "bleu-de-chanel", True,
     "Amaderado aromático, limpio y elegante para el día y la noche.",
     "Pomelo, limón, menta", "Jengibre, nuez moscada, jazmín", "Incienso, vetiver, cedro, sándalo", ["bleu-de-chanel-2"]),
    ("Eros", "Versace", "caballeros", "aromatica", "edt", 100, "98.00", "115.00", 22, "versace-eros", True,
     "Menta fresca y vainilla: intenso, dulce y con mucha proyección.",
     "Menta, manzana verde, limón", "Haba tonka, geranio, ambroxan", "Vainilla, vetiver, musgo de roble, cedro", []),
    ("Acqua di Giò", "Giorgio Armani", "caballeros", "acuatica", "edt", 100, "112.00", None, 9, "acqua-di-gio", True,
     "Cítrico marino y ligero, ideal para el calor de Panamá.",
     "Lima, limón, bergamota, notas marinas", "Jazmín, romero, fresia", "Almizcle blanco, cedro, pachulí", []),
    ("The One for Men", "Dolce & Gabbana", "caballeros", "oriental", "edp", 100, "105.00", "128.00", 4, "the-one-men", False,
     "Tabaco y ámbar con un toque especiado: cálido y sofisticado.",
     "Pomelo, cilantro, albahaca", "Cardamomo, jengibre, flor de naranjo", "Tabaco, ámbar, cedro", []),
    ("Luna Rossa Carbon", "Prada", "caballeros", "aromatica", "edt", 100, "120.00", None, 11, "luna-rossa-carbon", False,
     "Lavanda y notas minerales con un fondo limpio de ambroxan.",
     "Bergamota, pimienta", "Lavanda, notas metálicas", "Ambroxan, pachulí", []),
    ("Boss Bottled", "Hugo Boss", "caballeros", "amaderada", "edt", 100, "79.00", "92.00", 0, "boss-bottled", False,
     "Manzana y canela sobre maderas: un clásico versátil para la oficina.",
     "Manzana, ciruela, bergamota, limón", "Geranio, canela, clavo", "Vainilla, sándalo, cedro, vetiver", []),
    ("N°5", "Chanel", "damas", "floral", "edp", 100, "185.00", None, 8, "chanel-no5", True,
     "El floral aldehídico más icónico: jazmín, rosa y sándalo.",
     "Aldehídos, neroli, ylang-ylang", "Jazmín, rosa de mayo, lirio", "Sándalo, vetiver, vainilla", ["chanel-no5-2", "chanel-no5-3"]),
    ("Coco Mademoiselle", "Chanel", "damas", "chipre", "edp", 100, "172.00", None, 12, "coco-mademoiselle", True,
     "Chipre fresco con naranja, rosa y pachulí. Elegante sin ser pesado.",
     "Naranja, bergamota", "Rosa, jazmín", "Pachulí, vetiver, vainilla, almizcle blanco", ["coco-mademoiselle-2", "coco-mademoiselle-3"]),
    ("Coco Noir", "Chanel", "damas", "oriental", "edp", 100, "178.00", None, 3, "coco-noir", False,
     "Oriental profundo de rosa, pachulí e incienso para la noche.",
     "Bergamota, pomelo", "Rosa, jazmín, narciso", "Pachulí, sándalo, haba tonka, incienso", ["coco-noir-2"]),
    ("Gabrielle", "Chanel", "damas", "floral", "edp", 100, "160.00", "175.00", 7, "gabrielle", False,
     "Floral blanco y luminoso: jazmín, tuberosa y flor de naranjo.",
     "Mandarina, pomelo, grosella negra", "Jazmín, ylang-ylang, flor de naranjo, tuberosa", "Almizcle, sándalo", []),
    ("Black Opium", "Yves Saint Laurent", "damas", "gourmand", "edp", 90, "138.00", "156.00", 16, "black-opium", True,
     "Café negro y vainilla con flores blancas: adictivo y nocturno.",
     "Pera, pimienta rosa, flor de naranjo", "Café, jazmín, almendra amarga", "Vainilla, pachulí, cedro", []),
    ("La Vie Est Belle", "Lancôme", "damas", "gourmand", "edp", 100, "129.00", "148.00", 18, "la-vie-est-belle", True,
     "Iris y praliné: dulce, alegre y de larga duración.",
     "Grosella negra, pera", "Iris, jazmín, flor de naranjo", "Praliné, vainilla, pachulí, haba tonka", []),
    ("Miu Miu", "Miu Miu", "damas", "floral", "edp", 100, "96.00", None, 6, "miu-miu", False,
     "Lirio de los valles verde y rosa sobre un fondo amaderado suave.",
     "Lirio de los valles", "Rosa", "Akigalawood", []),
    ("Candy", "Prada", "damas", "gourmand", "edp", 80, "118.00", None, 2, "prada-candy", False,
     "Caramelo y benjuí: un gourmand cálido y envolvente.",
     "Caramelo", "Almizcle, benjuí", "Vainilla", []),
    ("Aqua Allegoria Mandarine Basilic", "Guerlain", "damas", "citrica", "edt", 125, "89.00", None, 13, "aqua-allegoria", False,
     "Mandarina y albahaca: chispeante, verde y perfecto para el día.",
     "Mandarina, naranja amarga", "Albahaca, té verde, manzanilla", "Sándalo, ámbar", []),
    ("The One", "Dolce & Gabbana", "damas", "oriental", "edp", 75, "119.00", "135.00", 10, "the-one-women", True,
     "Melocotón, lichi y vainilla en un oriental floral luminoso.",
     "Melocotón, lichi, mandarina, bergamota", "Lirio, jazmín, ciruela", "Vainilla, ámbar, almizcle, vetiver", []),
    ("Narciso", "Narciso Rodriguez", "damas", "floral", "edp", 90, "132.00", None, 5, "narciso-for-her", False,
     "Gardenia y rosa sobre almizcle blanco: sobrio y muy femenino.",
     "Rosa búlgara, gardenia", "Almizcle", "Cedro, vetiver, ámbar", []),
    ("Queen of Seduction", "Antonio Banderas", "damas", "floral", "edt", 80, "34.00", "42.00", 25, "queen-of-seduction", False,
     "Frambuesa y peonía: frutal floral, fresco y con gran precio.",
     "Frambuesa, bergamota, pimienta rosa", "Jazmín, peonía, rosa", "Almizcle, vainilla", []),
    ("Especially Escada", "Escada", "damas", "floral", "edp", 75, "85.00", None, 9, "especially-escada", False,
     "Rosa transparente con pera jugosa: ligero y alegre.",
     "Pera, semillas de ambreta", "Rosa, ylang-ylang", "Almizcle", []),
    ("Colonia Lavanda Suave", "Petit Atelier", "ninos", "aromatica", "edc", 100, "24.00", None, 20, "kids-lavanda", True,
     "Lavanda y flor de algodón para después del baño. Sin colorantes.",
     "Lavanda, bergamota", "Flor de algodón", "Almizcle suave", []),
    ("Bruma Algodón y Pera", "Petit Atelier", "ninos", "floral", "mist", 200, "19.00", "24.00", 15, "kids-bruma-pera", False,
     "Bruma corporal ligera con pera y algodón limpio.",
     "Pera, mandarina", "Algodón", "Almizcle blanco", []),
    ("Agua de Fresa y Flor", "Petit Atelier", "ninos", "gourmand", "edc", 100, "26.00", None, 4, "kids-fresa", False,
     "Fresa y flor de naranjo con un toque de vainilla suave.",
     "Fresa, mandarina", "Flor de naranjo", "Vainilla suave", []),
    ("Colonia Cítrica Menta", "Petit Atelier", "ninos", "citrica", "edc", 100, "22.00", "26.00", 12, "kids-citrica", False,
     "Limón y menta para refrescar en días de calor y de escuela.",
     "Limón, menta", "Hoja de naranjo", "Cedro suave", []),
]

LONG_DESC = (
    "{name} de {brand} es un {conc} de la familia {family}. {short} "
    "Lo recomendamos para {use}. Al aplicarlo, empieza con {top}; tras unos minutos aparece un corazón de "
    "{heart}, y en la piel permanece un fondo de {base}."
)
USE = {
    "caballeros": "uso diario, oficina y salidas de noche",
    "damas": "regalar o para usar en ocasiones especiales",
    "ninos": "después del baño; aplícalo sobre la ropa",
}

CUSTOMERS = [
    ("Ana Lucía", "Pérez"), ("Rodrigo", "Saldaña"), ("Itzel", "Batista"), ("Kevin", "Moreno"),
    ("Yariela", "Castillo"), ("Abdiel", "González"), ("Marisol", "De León"), ("Edwin", "Quintero"),
    ("Lourdes", "Him"), ("Nicole", "Arosemena"), ("Javier", "Chen"), ("Daniela", "Vergara"),
]
DISTRICTS = [
    ("panama", "San Francisco"), ("panama", "Bella Vista"), ("panama", "Juan Díaz"), ("panama-oeste", "Arraiján"),
    ("panama", "Betania"), ("chiriqui", "David"), ("cocle", "Penonomé"), ("colon", "Cristóbal"),
]


class Command(BaseCommand):
    help = "Carga datos de demostración de Nota Alta."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Borra los datos existentes antes de cargar.")

    @transaction.atomic
    def handle(self, *args, reset=False, **opts):
        if reset:
            Order.objects.all().delete()
            Product.objects.all().delete()
            Coupon.objects.all().delete()
            Brand.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_staff=False).delete()
        elif Product.objects.exists():
            self.stdout.write(self.style.WARNING("Ya hay productos. Usa --reset para recargar."))
            return

        rng = random.Random(7)
        cats = {}
        for i, (name, slug, tagline, image) in enumerate(CATEGORIES):
            cats[slug] = Category.objects.create(name=name, slug=slug, tagline=tagline, image_static=image, order=i)
        brands = {}
        for name, country, featured, desc in BRANDS:
            brands[name] = Brand.objects.create(
                name=name, slug=slugify(name), country=country, is_featured=featured, description=desc
            )

        now = timezone.now()
        products = []
        for i, (name, brand, cat, family, conc, ml, price, compare, stock, img, featured, short, top, heart, base, gallery) in enumerate(PRODUCTS):
            p = Product(
                name=name, slug=slugify(f"{brand} {name} {ml}ml"), brand=brands[brand], category=cats[cat],
                family=family, concentration=conc, volume_ml=ml, price=Decimal(price),
                compare_at_price=Decimal(compare) if compare else None, stock=stock,
                image_static=f"img/products/{img}.webp", is_featured=featured, short_description=short,
                notes_top=top, notes_heart=heart, notes_base=base,
            )
            p.description = LONG_DESC.format(
                name=name, brand=brand, conc=p.get_concentration_display().lower(),
                family=p.get_family_display().lower(), short=short, use=USE[cat],
                top=top.lower(), heart=heart.lower(), base=base.lower(),
            )
            p.save()
            Product.objects.filter(pk=p.pk).update(created_at=now - timedelta(days=60 - i * 2))
            for j, g in enumerate(gallery):
                ProductImage.objects.create(product=p, image_static=f"img/products/{g}.webp", alt=f"{brand} {name}, otra vista", order=j)
            products.append(p)

        Coupon.objects.create(code="NOTA10", percent_off=10, description="10% en todo el catálogo")
        Coupon.objects.create(code="DG10", percent_off=10, brand=brands["Dolce & Gabbana"], description="10% extra en Dolce & Gabbana")
        Coupon.objects.create(code="PETIT15", percent_off=15, brand=brands["Petit Atelier"], description="15% en colonias para niños")

        if not User.objects.filter(username="admin@notaalta.example").exists():
            User.objects.create_superuser("admin@notaalta.example", "admin@notaalta.example", "NotaAlta2026!", first_name="Equipo", last_name="Nota Alta")

        customers = []
        demo = User.objects.create_user("cliente@notaalta.example", "cliente@notaalta.example", "Cliente2026!", first_name="Mariela", last_name="Ríos")
        Profile.objects.create(user=demo, phone="6123-4567", province="panama", district="San Francisco", address="Calle 74, Edificio Brisas, apto 5B", reference="Frente al parque Omar")
        customers.append(demo)
        for first, last in CUSTOMERS:
            email = f"{slugify(first)}.{slugify(last)}@correo.example"
            u = User.objects.create_user(email, email, "Cliente2026!", first_name=first, last_name=last)
            prov, dist = rng.choice(DISTRICTS)
            Profile.objects.create(user=u, phone=f"6{rng.randint(100, 999)}-{rng.randint(1000, 9999)}", province=prov, district=dist, address=f"Calle {rng.randint(1, 80)}, casa {rng.randint(1, 120)}")
            customers.append(u)

        buyable = [p for p in products]
        for n in range(62):
            age_days = rng.uniform(0, 45)
            created = now - timedelta(days=age_days, hours=rng.randint(0, 10))
            user = demo if n % 9 == 0 else (rng.choice(customers) if rng.random() < 0.85 else None)
            prof = getattr(user, "profile", None) if user else None
            province, district = (prof.province, prof.district) if prof else rng.choice(DISTRICTS)
            ship = ShippingMethod.CIUDAD if province in ("panama", "panama-oeste") else ShippingMethod.INTERIOR
            if rng.random() < 0.15:
                ship = ShippingMethod.RETIRO
            pay = rng.choice([PaymentMethod.TARJETA, PaymentMethod.TARJETA, PaymentMethod.YAPPY, PaymentMethod.YAPPY, PaymentMethod.ACH]
                             + ([PaymentMethod.CONTRA_ENTREGA] if ship == ShippingMethod.CIUDAD else []))
            if age_days > 8:
                status = rng.choice([Order.Status.ENTREGADO] * 8 + [Order.Status.CANCELADO])
            elif age_days > 3:
                status = rng.choice([Order.Status.ENVIADO, Order.Status.ENTREGADO, Order.Status.PREPARANDO])
            else:
                status = rng.choice([Order.Status.PENDIENTE, Order.Status.PAGADO, Order.Status.PREPARANDO])
            lines = rng.sample(buyable, rng.choice([1, 1, 1, 2, 2, 3]))
            items = [(p, rng.choice([1, 1, 1, 2])) for p in lines]
            subtotal = sum((p.price * q for p, q in items), Decimal("0"))
            discount = (subtotal * Decimal("0.10")).quantize(Decimal("0.01")) if rng.random() < 0.2 else Decimal("0")
            ship_cost = shipping_cost(ship, subtotal - discount)
            name = user.get_full_name() if user else rng.choice(["Carlos Ortega", "Gisela Ramos", "Luis Him", "Paola Ríos"])
            order = Order.objects.create(
                user=user, full_name=name, email=user.email if user else f"{slugify(name)}@correo.example",
                phone=prof.phone if prof else "6555-0101", province=province, district=district,
                address=prof.address if prof else "Vía España, local 3", shipping_method=ship, payment_method=pay,
                status=status, coupon_code="NOTA10" if discount else "", subtotal=subtotal, discount=discount,
                shipping_cost=ship_cost, total=subtotal - discount + ship_cost,
            )
            for p, q in items:
                OrderItem.objects.create(order=order, product=p, product_name=str(p), unit_price=p.price, quantity=q)
            Order.objects.filter(pk=order.pk).update(created_at=created, updated_at=created)

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {len(products)} perfumes, {len(brands)} marcas, {len(customers)} clientes y 62 pedidos de demostración."
        ))
