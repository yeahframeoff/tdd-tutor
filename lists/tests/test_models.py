from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        the_list = List()
        the_list.save()

        text1 = 'The first (ever) list item'
        item = Item()
        item.text = text1
        item.list = the_list
        item.save()
        
        text2 = 'Item the second'
        item = Item()
        item.text = text2
        item.list = the_list
        item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, the_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        saved_item1 = saved_items[0]
        saved_item2 = saved_items[1]
        self.assertEqual(saved_item1.text, text1)
        self.assertEqual(saved_item1.list, the_list)
        self.assertEqual(saved_item2.text, text2)
        self.assertEqual(saved_item2.list, the_list)

    def test_cannot_save_empty_list_items(self):
        the_list = List.objects.create()
        item = Item(list=the_list, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        the_list = List.objects.create()
        self.assertEqual(the_list.get_absolute_url(), '/lists/%d/' % the_list.id)
