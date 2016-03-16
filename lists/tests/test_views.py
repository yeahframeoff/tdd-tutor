from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.utils.html import escape

from lists.views import home_page
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='das item eins', list=correct_list)
        Item.objects.create(text='das item zwei', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='anderes item eins', list=other_list)
        Item.objects.create(text='anderes item zwei', list=other_list)

        response = self.client.get('/lists/%d/' % correct_list.id)

        self.assertContains(response, 'das item eins')
        self.assertContains(response, 'das item zwei')
        self.assertNotContains(response, 'anderes item eins')
        self.assertNotContains(response, 'anderes item zwei')

    def test_uses_list_template(self):
        the_list = List.objects.create()
        response = self.client.get('/lists/%d/' % the_list.id)
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % correct_list.id)
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'text': 'A new item for an exisitng list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an exisitng list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'text': 'A new item for an exisitng list'}
        )

        self.assertRedirects(response, '/lists/%d/' % correct_list.id)

    def test_displays_item_form(self):
        the_list = List.objects.create()
        response = self.client.get('/lists/%d/' % the_list.id)
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    def send_invalid_input_POST_request(self):
        the_list = List.objects.create()

        return self.client.post(
            '/lists/%d/' % the_list.id,
            data={'text': ''}
        )

    def test_for_invalid_saves_nothing_to_db(self):
        response = self.send_invalid_input_POST_request()
        self.assertEqual(Item.objects.count(), 0)
    
    def test_for_invalid_input_renders_list_template(self):
        response = self.send_invalid_input_POST_request()
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
    
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.send_invalid_input_POST_request()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
    
    def test_for_invalid_passes_form_to_template(self):
        response = self.send_invalid_input_POST_request()
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new', 
            data={'text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new', 
            data={'text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % new_list.id)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
