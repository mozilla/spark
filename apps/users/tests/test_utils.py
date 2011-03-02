from nose.tools import eq_

from spark.tests import TestCase

from users.models import User, UserNode
from users.utils import user_node, create_relationship


class UtilsCase(TestCase):
    fixtures = ['boost.json']
    
    def test_user_node_retrieves_node(self):
        user = User.objects.get(username='franck')
        node = user_node(user)
        
        assert node == UserNode.objects.get(user=user)
    
    def test_user_node_creates_a_node(self):
        user = User(username='new_user')
        user.save()
        qs = UserNode.objects.filter(user=user)
        eq_(0, len(qs))
        
        node = user_node(user)
        eq_(node, user.node)

    def test_create_relationship(self):
        child = User.objects.get(username='bob')
        eq_(None, child.node.parent)
        
        parent = User.objects.get(username='john')
        created = create_relationship(parent, child)
        
        eq_(True, created)
        eq_(child.node.parent, parent.node)
    
    def test_create_invalid_relationship(self):
        """ Should not create relationship:
            franck is already a child of bob in the fixture data.
        """
        parent = User.objects.get(username='franck')
        child = User.objects.get(username='bob')
        
        created = create_relationship(parent, child)
        eq_(False, created)