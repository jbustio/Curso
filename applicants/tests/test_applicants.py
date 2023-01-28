from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.company = cls.env['res.partner'].create({
            'name': 'company'
        })

        cls.applicants = cls.env['applicants.applicants'].create([
            {
                'name': 'John',
                'lastName1': 'Doe',
                'lastName2': 'Daryll',
                'CI': 95111428926,
                'address': 'Somewhere',
                'Age': 20,
                'Sex': 'Male',
                'company_id': cls.company.id
            },
            {
                'name': 'Jane',
                'lastName1': 'Doe',
                'lastName2': 'Doe',
                'CI': 95111431544,
                'address': 'Somewhere',
                'Age': 20,
                'Sex': 'Female',
                'company_id': cls.company.id
            }
        ])
        cls.technology_and_exp = cls.env['applicants.technology_and_exp'].create([{
            'name': 'VueJs',
            'applicant_id': cls.applicants[0].id,
            'experience_years': 3
        }, 
        {
            'name': 'Python',
            'applicant_id': cls.applicants[1].id,
            'experience_years': 4
        }])



    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
           {'name': ..., 'total_area': ...},
           {'name': ..., 'total_area': ...},
        ])


    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        self.properties.action_sold()
        self.assertRecordValues(self.properties, [
           {'name': ..., 'state': ...},
           {'name': ..., 'state': ...},
        ])

        with self.assertRaises(UserError):
            self.properties.forbidden_action_on_sold_property()