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
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        
        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


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


class ListViewTest(TestCase):

    def test_displays_all_list_items(self):
        Item.objects.create(text='das item eins')
        Item.objects.create(text='das item zwei')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'das item eins')
        self.assertContains(response, 'das item zwei')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
