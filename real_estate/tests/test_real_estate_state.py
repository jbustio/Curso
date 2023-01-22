from odoo.tests.common import TransactionCase

class TestRealEstate(TransactionCase):
    def setUp(self,*args,**kwargs):
        super(TestRealEstate, self).setUp(*args,**kwargs)
        self.test_real_estate = self.env['real_estate.real_estate'].create({
            'name':'Prueba',
            'description':"""
            Esta es una instancia de prueba creada mediante un test automatizado
            """,
            'expected_price':20000,
            'selling_price':25000,  
        })

    def test_button_north(self):
        """Make north button"""
        self.test_real_estate.north_direction()
        self.assertEqual(self.test_real_estate.garden_direction,'NEast',
        "The field should be changed to north") 

    def test_button_south(self):
        """Make south button"""
        self.test_real_estate.north_direction()
        self.assertEqual(self.test_real_estate.garden_direction,'South',
        "The field should be changed to south")