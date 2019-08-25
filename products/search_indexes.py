from haystack import indexes
from products.models import StoreInventory, Product, GeneralItemDictionary


class ProductIndex (indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    #useful when used to filter search options
    generalItem = indexes.CharField(model_attr='generalItem')
    additionalName = indexes.CharField(model_attr='additionalName')
    colorway = indexes.CharField(model_attr='colorway')
    #----------------------------------------

    def get_model(self):
        return Product

    #def index_Queryset(self, using=None):
        #used when entire index for model is updated
    #    return self.get_model.objects.all()