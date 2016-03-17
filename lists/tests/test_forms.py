from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR, ExistingListItemForm, DUPLICATE_ITEM_ERROR
from lists.models import List, Item


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_a_list(self):
        the_list = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=the_list)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, the_list)


class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        the_list = List.objects.create()
        form = ExistingListItemForm(for_list=the_list)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        the_list = List.objects.create()
        form = ExistingListItemForm(for_list=the_list, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        the_list = List.objects.create()
        item = Item.objects.create(list=the_list, text='keine Blisniaschke')
        form = ExistingListItemForm(for_list=the_list, data={'text': 'keine Blisniaschke'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save_handles_saving_a_list(self):
        the_list = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=the_list)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, the_list)

    def test_form_save(self):
        the_list = List.objects.create()
        form = ExistingListItemForm(for_list=the_list, data={'text': 'Goedendag'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
