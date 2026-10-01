import json

from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from django.views import View

from .models import Category, Customer, Order, OrderDetail, Product, Supplier


class HealthView(View):
    def get(self, request):
        status = {'application': 'ok', 'database': 'error', 'cache': 'error'}

        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            status['database'] = 'ok'
        except Exception:
            pass

        try:
            cache.set('health_check', 'ok', 10)
            if cache.get('health_check') == 'ok':
                status['cache'] = 'ok'
        except Exception:
            pass

        ok = all(v == 'ok' for v in status.values())
        return JsonResponse(status, status=200 if ok else 503)


class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all().order_by('id')
        return JsonResponse([c.to_dict() for c in categories], safe=False)


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all().order_by('id')
        return JsonResponse([p.to_dict() for p in products], safe=False)


class SupplierListView(View):
    def get(self, request):
        suppliers = Supplier.objects.all().order_by('id')
        return JsonResponse([s.to_dict() for s in suppliers], safe=False)


class CustomerListView(View):
    def get(self, request):
        customers = Customer.objects.all().order_by('id')
        return JsonResponse([c.to_dict() for c in customers], safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        required = ['company_name']
        for field in required:
            if field not in data:
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)

        customer = Customer.objects.create(
            company_name=data['company_name'],
            contact_name=data.get('contact_name'),
            contact_title=data.get('contact_title'),
            address=data.get('address'),
            city=data.get('city'),
            region=data.get('region'),
            postal_code=data.get('postal_code'),
            country=data.get('country'),
            phone=data.get('phone'),
            fax=data.get('fax'),
        )
        return JsonResponse(customer.to_dict(), status=201)


class CustomerDetailView(View):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        return JsonResponse(customer.to_dict())

    def delete(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        customer.delete()
        return JsonResponse({'status': 'deleted'}, status=204)


class CustomerOrdersView(View):
    def get(self, request, customer_id):
        try:
            Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        orders = Order.objects.filter(customer_id=customer_id).order_by('-order_date')
        return JsonResponse([o.to_dict() for o in orders], safe=False)


class OrderListView(View):
    def get(self, request):
        orders = Order.objects.all().order_by('-order_date')[:100]
        return JsonResponse([o.to_dict() for o in orders], safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if 'customer_id' not in data:
            return JsonResponse({'error': 'Missing required field: customer_id'}, status=400)

        try:
            Customer.objects.get(id=data['customer_id'])
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        order = Order.objects.create(
            customer_id=data['customer_id'],
            order_date=data.get('order_date'),
            required_date=data.get('required_date'),
            shipped_date=data.get('shipped_date'),
            shipper_id=data.get('shipper_id'),
            freight=data.get('freight', 0),
            ship_name=data.get('ship_name'),
            ship_address=data.get('ship_address'),
            ship_city=data.get('ship_city'),
            ship_region=data.get('ship_region'),
            ship_postal_code=data.get('ship_postal_code'),
            ship_country=data.get('ship_country'),
        )

        for detail in data.get('order_details', []):
            OrderDetail.objects.create(
                order=order,
                product_id=detail.get('product_id'),
                unit_price=detail.get('unit_price', 0),
                quantity=detail.get('quantity', 1),
                discount=detail.get('discount', 0),
            )

        return JsonResponse(order.to_dict(include_details=True), status=201)


class OrderDetailView(View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        return JsonResponse(order.to_dict(include_details=True))
