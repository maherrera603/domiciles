from django.db.models import Manager


class ShopsManager(Manager):

    def obtain_all_shops(self):
        return self.all()

    def get_data_shops(self, user):
        return self.get(user=user)

    def obtain_all_shops_by_search(self, search=None):
        shops = self.filter(shop__icontains=search) if search else self.all()
        return shops

    def create_enterprise(self, user, form):
        shop = form.cleaned_data['shop']
        nit = form.cleaned_data['nit']
        phone = form.cleaned_data['phone']
        return self.create(shop=shop, nit=nit, phone=phone, user=user)

    def get_user(self, user):
        return self.get(user=user)

    def get_shop_by_id(self, pk):
        return self.get(pk=pk)
