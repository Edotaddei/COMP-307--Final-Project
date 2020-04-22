from django.test import TestCase
from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Product, OrderProduct, Order, Address, TradeProduct, TradeRequest

# Create your tests here.
class ProductTest(TestCase):

	def test_fields(self):
		user = User.objects.create_user("TestUser", "user@test.com", "testpword")
		testProd= Product.objects.create(name="TestProduct", owner= user, description="Testing product", price=50, count=10, category="furniture")
		testProd.save()

		prod = Product.objects.get(name="TestProduct")
		self.assertEqual(prod, testProd)

class OrderProductTest(TestCase):

	def test_fields(self):
		user = User.objects.create_user("TestUser", "user@test.com", "testpword")
		prod= Product.objects.create(name="TestProduct", owner= user, description="Testing product", price=50, count=10, category="furniture")
		testOrderProduct=OrderProduct.objects.create(is_ordered=True, product=prod, count=10)

		orderProduct=OrderProduct.objects.get(product=prod)

		self.assertEqual(orderProduct, testOrderProduct)

	def test_get_product_count_price(self):

		user = User.objects.create_user("TestUser", "user@test.com", "testpword")
		prod= Product.objects.create(name="TestProduct", owner= user, description="Testing product", price=50, count=10, category="furniture")
		testOrderProduct=OrderProduct.objects.create(is_ordered=True, product=prod, count=10)

		self.assertEqual(testOrderProduct.get_product_count_price(), 500)

class OrderTest(TestCase):

	def test_fields(self):
		user = User.objects.create_user("TestUser", "user@test.com", "testpword")
		user2 = User.objects.create_user("TestUser2", "user2@test.com", "testpword2")
		prod= Product.objects.create(name="TestProduct", owner= user, description="Testing product", price=50, count=10, category="furniture")
		testOrderProduct= OrderProduct.objects.create(is_ordered=True, product=prod, count=10)

		testOrder=Order.objects.create(owner=user2, date=timezone.now(), is_ordered=True)
		testOrder.products.add(testOrderProduct)

		order= Order.objects.get(owner=user2)
		self.assertEqual(order, testOrder)

	def test_get_total_price(self):

		user = User.objects.create_user("TestUser", "user@test.com", "testpword")
		user2 = User.objects.create_user("TestUser2", "user2@test.com", "testpword2")
		prod= Product.objects.create(name="TestProduct", owner= user, description="Testing product", price=50, count=10, category="furniture")
		testOrderProduct= OrderProduct.objects.create(is_ordered=True, product=prod, count=10)

		testOrder=Order.objects.create(owner=user2, date=timezone.now(), is_ordered=True)
		testOrder.products.add(testOrderProduct)

		self.assertEqual(testOrder.get_total_price(), 500)

class AddressTest(TestCase):

	def test_fields(self):

		user = User.objects.create_user("TestUser", "user@test.com", "testpword")
		user2 = User.objects.create_user("TestUser2", "user2@test.com", "testpword2")
		prod= Product.objects.create(name="TestProduct", owner= user, description="Testing product", price=50, count=10, category="furniture")
		testOrderProduct= OrderProduct.objects.create(is_ordered=True, product=prod, count=10)

		testOrder=Order.objects.create(owner=user2, date=timezone.now(), is_ordered=True)
		testOrder.products.add(testOrderProduct)


		testAddress = Address.objects.create(order=testOrder, street="TestStreet", number="123", city="Montreal", zip="TEST12", country="Montreal")

		address = Address.objects.get(order=testOrder)

		self.assertEqual(testAddress, address) 
	
class TradeProductTest(TestCase):

	def test_fields(self):
		user = User.objects.create_user("TestUser", "user@test.com", "testpword")
		prod= Product.objects.create(name="TestProduct", owner= user, description="Testing product", price=50, count=10, category="furniture")
		testTradeProduct=TradeProduct.objects.create(product=prod, is_ordered=False)

		tradeProduct = TradeProduct.objects.get(product=prod)

		self.assertEqual(tradeProduct, testTradeProduct)
	
		
class TradeRequestTest(TestCase):

	def test_fields(self):

		user = User.objects.create_user("TestUser", "user@test.com", "testpword")
		user2 = User.objects.create_user("TestUser2", "user2@test.com", "testpword2")
		prod= Product.objects.create(name="TestProduct", owner= user, description="Testing product", price=50, count=10, category="furniture")
		tradeProduct=TradeProduct.objects.create(product=prod, is_ordered=False)

		testTradeRequest = TradeRequest.objects.create(requester=user2, receiver_username="TestUser", is_accepted=False, is_rejected=False, is_concluded=False)
		testTradeRequest.products.add(tradeProduct)

		tradeRequest= TradeRequest.objects.get(requester=user2)

		self.assertEqual(tradeRequest, testTradeRequest)
	
