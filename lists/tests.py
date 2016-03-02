from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page

from lists.models import Item


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
    
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        
        response = home_page(request)
        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        self.assertEqual(response.content.decode(), expected_html)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        text1 = 'The first (ever) list item'
        item = Item()
        item.text = text1
        item.save()
        
        text2 = 'Item the second'
        item = Item()
        item.text = text2
        item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        saved_item1 = saved_items[0]
        saved_item2 = saved_items[1]
        self.assertEqual(saved_item1.text, text1)
        self.assertEqual(saved_item2.text, text2)
