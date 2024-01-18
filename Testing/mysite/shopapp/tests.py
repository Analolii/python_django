from django.contrib.auth.models import User, Permission
from django.test import TestCase


from django.urls import reverse

from shopapp.models import Product, Order
from random import choices
from string import ascii_letters


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='Vova',
            password='123',
        )
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.product_ordered = Product.objects.create(
            pk=1,
            name='Smartphone',
            description='Black',
            price=999,
            discount=5,
        )

        self.test_order = Order.objects.create(
            id=1,
            delivery_address='Milan',
            promocode="".join(choices(ascii_letters, k=10)),
            user=self.user,
        )
        self.test_order.products.set([self.product_ordered])

    def test_order_details(self):
        response = self.client.get(

            reverse('shopapp:order_details', kwargs={'pk': self.test_order.pk}),
            {
                'products': self.product_ordered,
                'delivery_address': self.test_order.delivery_address,
                'promocode': self.test_order.promocode,
            },
        )
        self.assertContains(response, self.test_order.delivery_address)
        self.assertContains(response, self.test_order.promocode)
        self.assertEqual(self.test_order.pk, response.context['order'].pk)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'orders-fixture.json',
        'products-fixture.json',
        'users-fixture.json'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='Vova',
            password='123',
            is_staff=True,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_orders_export(self):
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.pk,
                'products': [product.pk for product in order.products.all()],
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(orders_data['orders'], expected_data)


# Create your tests here.
