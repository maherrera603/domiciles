import datetime
from django.db.models import Manager


class ProductManager(Manager):

    def obtain_all_products_by_search(self, search, pk):
        if search is not None:
            return self.filter(product__icontains=search, shop=pk)
        return self.filter(shop=pk)

    def saveProduct(self, shop, form):
        product = form.cleaned_data['product']
        description = form.cleaned_data['description']
        avatar = form.cleaned_data['avatar']
        price = form.cleaned_data['price']
        quantity = form.cleaned_data['quantity']
        return self.create(
                product=product, description=description,
                avatar=avatar, price=price,
                quantity=quantity, shop=shop
                )

    def get_product(self, pk):
        return self.get(pk=pk)

    def delete_product(self, product) -> bool:
        return True if product.delete() else False


class OrderManager(Manager):

    def add_order(self, product, shop, client):
        full_value = product.price * 1
        return self.create(
                product=product, shop=shop,
                client=client, full_value=full_value
                )

    def get_orders_by_client(self, client, search=None):
        if search is not None:
            return self.filter(client=client, shop__shop__icontains=search).exclude(status=3).distinct('shop')
        return self.filter(client=client).exclude(status=3).distinct('shop')

    def get_products_of_orders(self, client, shop):
        return self.filter(client=client, shop=shop)

    def get_price_total_orders(self, client, shop) -> float:
        products = self.filter(client=client, shop=shop)
        total: float = 0
        for product in products:
            total += product.product.price * product.quantity
        return total

    def get_order(self, shop, pk):
        return self.get(shop=shop, pk=pk)

    def get_clients_by_order(self, shop):
        return self.filter(shop=shop, status=2).distinct('client')

    def update_status_buy(self, shop, client):
        return self.filter(shop=shop, client=client)

    def get_orders_by_status_and_dateSold(self, shop, dateSold):
        if dateSold:
            dateFormat = datetime.datetime.strptime(dateSold, '%Y-%m-%d').date()
            return self.filter(shop=shop, status=3, date_add=dateFormat)
        return self.filter(shop=shop, status=3)
