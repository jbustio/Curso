from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from psycopg2 import IntegrityError
from odoo.tests import tagged
import openerp.tools

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


    @openerp.tools.mute_logger('openerp.sql_db')
    def test_repeated_tech_by_applicant(self):
        """Test that the tech cannot be re-entered by an applicant."""
        with self.assertRaises(IntegrityError):
            self.env['applicants.technology_and_exp'].create([{
                'name': 'VueJs',
                'applicant_id': self.__class__.applicants[0].id,
                'experience_years': 3
            }])

