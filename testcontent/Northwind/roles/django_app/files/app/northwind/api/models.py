from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


class Supplier(models.Model):
    company_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_title = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suppliers'

    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'contact_name': self.contact_name,
            'contact_title': self.contact_title,
            'address': self.address,
            'city': self.city,
            'region': self.region,
            'postal_code': self.postal_code,
            'country': self.country,
            'phone': self.phone,
            'fax': self.fax,
        }


class Product(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, db_column='supplier_id')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, db_column='category_id')
    quantity_per_unit = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    units_in_stock = models.IntegerField(default=0)
    units_on_order = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=0)
    discontinued = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'products'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'supplier_id': self.supplier_id,
            'category_id': self.category_id,
            'quantity_per_unit': self.quantity_per_unit,
            'unit_price': str(self.unit_price),
            'units_in_stock': self.units_in_stock,
            'units_on_order': self.units_on_order,
            'reorder_level': self.reorder_level,
            'discontinued': self.discontinued,
        }


class Customer(models.Model):
    company_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_title = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'

    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'contact_name': self.contact_name,
            'contact_title': self.contact_title,
            'address': self.address,
            'city': self.city,
            'region': self.region,
            'postal_code': self.postal_code,
            'country': self.country,
            'phone': self.phone,
            'fax': self.fax,
        }


class Shipper(models.Model):
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shippers'

    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'phone': self.phone,
        }


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, db_column='customer_id')
    order_date = models.DateField(blank=True, null=True)
    required_date = models.DateField(blank=True, null=True)
    shipped_date = models.DateField(blank=True, null=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True, db_column='shipper_id')
    freight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ship_name = models.CharField(max_length=100, blank=True, null=True)
    ship_address = models.CharField(max_length=200, blank=True, null=True)
    ship_city = models.CharField(max_length=50, blank=True, null=True)
    ship_region = models.CharField(max_length=50, blank=True, null=True)
    ship_postal_code = models.CharField(max_length=20, blank=True, null=True)
    ship_country = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'

    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'customer_id': self.customer_id,
            'order_date': str(self.order_date) if self.order_date else None,
            'required_date': str(self.required_date) if self.required_date else None,
            'shipped_date': str(self.shipped_date) if self.shipped_date else None,
            'shipper_id': self.shipper_id,
            'freight': str(self.freight),
            'ship_name': self.ship_name,
            'ship_address': self.ship_address,
            'ship_city': self.ship_city,
            'ship_region': self.ship_region,
            'ship_postal_code': self.ship_postal_code,
            'ship_country': self.ship_country,
        }
        if include_details:
            data['order_details'] = [d.to_dict() for d in self.orderdetail_set.all()]
        return data


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_id')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, db_column='product_id')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        managed = False
        db_table = 'order_details'

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'unit_price': str(self.unit_price),
            'quantity': self.quantity,
            'discount': str(self.discount),
        }
