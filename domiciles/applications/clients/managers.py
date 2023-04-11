from django.db.models import Manager


class ClientManagers(Manager):

    def register(self, form, user):
        name = form.cleaned_data['name']
        lastname = form.cleaned_data['lastname']
        type_document = form.cleaned_data['type_document']
        document = form.cleaned_data['document']
        phone = form.cleaned_data['phone']
        client = self.create(
                name=name, lastname=lastname,
                type_document=type_document, document=document,
                phone=phone, user=user
                )
        return client

    def get_client(self, user):
        return self.get(user=user)

    def get_client_by_id(self, pk):
        return self.get(pk=pk)
