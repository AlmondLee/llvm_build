# Check that the LNT REST JSON API is working.
# create temporary instance
# RUN: rm -rf %t.instance
# RUN: python %{shared_inputs}/create_temp_instance.py \
# RUN:     %s %{shared_inputs}/SmallInstance \
# RUN:     %t.instance %S/Inputs/V4Pages_extra_records.sql
#
# RUN: python %s %t.instance

from V4Pages import check_json
import lnt.server.db.migrate
import lnt.server.ui.app
import logging
import sys
import unittest
import yaml

logging.basicConfig(level=logging.DEBUG)

machines_expected_response = [{u'hardware': u'x86_64',
                               u'os': u'Darwin 11.3.0',
                               u'id': 1,
                               u'name': u'localhost__clang_DEV__x86_64',
                               u'hostname': u'localhost',
                               u'uname': u'Darwin localhost 11.3.0 Darwin Kernel Version 11.3.0: Thu Jan 12'
                                         u' 18:47:41 PST 2012; root:xnu-1699.24.23~1/RELEASE_X86_64 x86_64'},
                              {u'hardware': u'AArch64',
                               u'os': u'linux',
                               u'id': 2,
                               u'name': u'machine2'},
                              {u'hardware': u'AArch64',
                               u'os': u'linux',
                               u'id': 3,
                               u'name': u'machine3'}]

order_expected_response = {u'llvm_project_revision': u'154331',
                           u'id': 1}

sample_expected_response = {u'id': 1,
                            u'execution_time': 0.0003,
                            u'test_id': 1,
                            u'compile_time': 0.007}

graph_data = [[[152292], 1.0,
               {u'date': u'2012-05-01 16:28:23',
                u'label': u'152292',
                u'runID': u'5'}],
              [[152293], 10.0,
               {u'date': u'2012-05-03 16:28:24',
                u'label': u'152293',
                u'runID': u'6'}]]

graph_data2 = [[[152293], 10.0,
                {u'date': u'2012-05-03 16:28:24',
                 u'label': u'152293',
                 u'runID': u'6'}]]

possible_run_keys = {
    u'ARCH',
    u'CC_UNDER_TEST_IS_CLANG',
    u'CC_UNDER_TEST_TARGET_IS_X86_64',
    u'DISABLE_CBE',
    u'DISABLE_JIT',
    u'ENABLE_HASHED_PROGRAM_OUTPUT',
    u'ENABLE_OPTIMIZED',
    u'LLC_OPTFLAGS',
    u'LLI_OPTFLAGS',
    u'OPTFLAGS',
    u'TARGET_CC',
    u'TARGET_CXX',
    u'TARGET_FLAGS',
    u'TARGET_LLVMGCC',
    u'TARGET_LLVMGXX',
    u'TEST',
    u'USE_REFERENCE_OUTPUT',
    u'__report_version__',
    u'cc1_exec_hash',
    u'cc_alt_src_branch',
    u'cc_alt_src_revision',
    u'cc_as_version',
    u'cc_build',
    u'cc_exec_hash',
    u'cc_ld_version',
    u'cc_name',
    u'cc_src_branch',
    u'cc_src_revision',
    u'cc_target',
    u'cc_version',
    u'cc_version_number',
    u'end_time',
    u'id',
    u'inferred_run_order',
    u'llvm_project_revision',
    u'no_errors',
    u'order_by',
    u'order_id',
    u'start_time',
    u'sw_vers',
    u'test_suite_revision',
}

possible_machine_keys = {u'name',
                         u'hostname',
                         u'hardware',
                         u'os',
                         u'id',
                         u'uname'}


class JSONAPITester(unittest.TestCase):
    """Test the REST api."""

    def setUp(self):
        """Bind to the LNT test instance."""
        _, instance_path = sys.argv
        self.instance_path = instance_path
        app = lnt.server.ui.app.App.create_standalone(instance_path)
        app.testing = True
        self.client = app.test_client()

    def _check_response_is_well_formed(self, response):
        """API Should always return the generated by field in the top level dict."""
        # All API calls should return a top level dict.
        self.assertEqual(type(response), dict)

        # There should be no unexpected top level keys.
        all_top_level_keys = {'generated_by', 'machine', 'machines', 'runs', 'run', 'orders', 'tests', 'samples'}
        keys = set(response.keys())
        self.assertTrue(keys.issubset(all_top_level_keys),
                        "{} not subset of {}".format(keys, all_top_level_keys))
        # All API calls should return as generated by.
        self.assertIn("LNT Server v", response['generated_by'])

    def test_machine_api(self):
        """Check /machines/ and /machines/n return expected results from testdb.
        """
        client = self.client

        # All machines returns the list of machines with parameters, but no runs.
        j = check_json(client, 'api/db_default/v4/nts/machines/')
        self._check_response_is_well_formed(j)
        self.assertEquals(j['machines'], machines_expected_response)
        self.assertIsNone(j.get('runs'))

        j = check_json(client, 'api/db_default/v4/nts/machines')
        self._check_response_is_well_formed(j)
        self.assertEquals(j['machines'], machines_expected_response)
        self.assertIsNone(j.get('runs'))

        # Machine + properties + run information.
        j = check_json(client, 'api/db_default/v4/nts/machines/1')
        self._check_response_is_well_formed(j)
        self.assertEqual(j['machine'], machines_expected_response[0])

        self.assertEqual(len(j['runs']), 2)
        for run in j['runs']:
            self.assertSetEqual(set(run.keys()), possible_run_keys)

        # Specify machine by name
        j = check_json(client, 'api/db_default/v4/nts/machines/localhost__clang_DEV__x86_64')
        self._check_response_is_well_formed(j)
        self.assertEqual(j['machine'], machines_expected_response[0])

        # Invalid machine ids are 404.
        check_json(client, 'api/db_default/v4/nts/machines/99', expected_code=404)
        check_json(client, 'api/db_default/v4/nts/machines/foo', expected_code=404)

    def test_run_api(self):
        """Check /runs/n returns expected run information."""
        client = self.client
        j = check_json(client, 'api/db_default/v4/nts/runs/1')
        self._check_response_is_well_formed(j)
        expected = {"end_time": "2012-04-11T16:28:58",
                    "start_time": "2012-04-11T16:28:23",
                    "id": 1,
                    "llvm_project_revision": u'154331'}
        self.assertDictContainsSubset(expected, j['run'])
        self.assertEqual(len(j['tests']), 2)
        # This should not be a run.
        check_json(client, 'api/db_default/v4/nts/runs/100', expected_code=404)

    def test_order_api(self):
        """ Check /orders/n returns the expected order information."""
        client = self.client
        j = check_json(client, 'api/db_default/v4/nts/orders/1')
        self.assertEquals(j['orders'][0], order_expected_response)
        self._check_response_is_well_formed(j)
        check_json(client, 'api/db_default/v4/nts/orders/100', expected_code=404)

    def test_single_sample_api(self):
        """ Check /samples/n returns the expected sample information."""
        client = self.client
        j = check_json(client, 'api/db_default/v4/nts/samples/1')
        self._check_response_is_well_formed(j)
        self.assertEquals(sample_expected_response, j['samples'][0])
        check_json(client, 'api/db_default/v4/nts/samples/1000', expected_code=404)

    def test_graph_api(self):
        """Check that /graph/x/y/z returns what we expect."""
        client = self.client

        j = check_json(client, 'api/db_default/v4/nts/graph/2/4/2')
        # TODO: Graph API needs redesign to be well formed.
        # self._check_response_is_well_formed(j)
        self.assertEqual(graph_data, j)

        # Now check that limit works.
        j2 = check_json(client, 'api/db_default/v4/nts/graph/2/4/2?limit=1')
        # self._check_response_is_well_formed(j)
        self.assertEqual(graph_data2, j2)

    def test_samples_api(self):
        """Samples API."""
        client = self.client
        # Run IDs must be passed, so 400 if they are not.
        check_json(client, 'api/db_default/v4/nts/samples',
                   expected_code=400)

        # Simple single run.
        j = check_json(client, 'api/db_default/v4/nts/samples?runid=1')
        self._check_response_is_well_formed(j)
        expected = [
            {u'compile_time': 0.007, u'llvm_project_revision': u'154331',
             u'name': u'SingleSource/UnitTests/2006-12-01-float_varg',
             u'run_id': 1, u'execution_time': 0.0003, u'id': 1},
            {u'compile_time': 0.0072, u'llvm_project_revision': u'154331',
             u'name': u'SingleSource/UnitTests/2006-12-04-DynAllocAndRestore',
             u'run_id': 1,
             u'execution_time': 0.0003,
             u'id': 2}]

        self.assertEqual(j['samples'], expected)

        # Check that other args are ignored.
        extra_param = check_json(client,
                                 'api/db_default/v4/nts/samples?runid=1&foo=bar')
        self._check_response_is_well_formed(extra_param)
        self.assertEqual(j, extra_param)
        # There is only one run in the DB.
        two_runs = check_json(client,
                              'api/db_default/v4/nts/samples?runid=1&runid=2')
        self._check_response_is_well_formed(two_runs)
        self.assertEqual(j, two_runs)

    def test_fields_api(self):
        """Fields API."""
        client = self.client
        j = check_json(client, 'api/db_default/v4/nts/fields')

        fields = j['fields']

        # check number of fields
        self.assertEqual(9, len(fields))

        # check first field
        f0 = fields[0]
        self.assertEqual(0, f0['column_id'])
        self.assertEqual('compile_time', f0['column_name'])

    def test_tests_api(self):
        """Tests API."""
        client = self.client
        j = check_json(client, 'api/db_default/v4/nts/tests')

        tests = j['tests']

        # check number of tests
        self.assertEqual(9, len(tests))

        # check first test
        t0 = tests[0]
        self.assertEqual(1, t0['id'])
        self.assertEqual('SingleSource/UnitTests/2006-12-01-float_varg', t0['name'])

    def test_schema(self):
        client = self.client
        rest_schema = check_json(client, 'api/db_default/v4/nts/schema')

        # The reported schema should be the same as the yaml one on the top.
        with open('%s/schemas/nts.yaml' % self.instance_path) as syaml:
            yaml_schema = yaml.load(syaml)
            # Do some massaging to make it similar to the rest API result.
            for m in yaml_schema['metrics']:
                if 'unit' not in m:
                    m['unit'] = None
                if 'unit_abbrev' not in m:
                    m['unit_abbrev'] = None
                if 'display_name' not in m:
                    m['display_name'] = m['name']
                if 'bigger_is_better' not in m:
                    m['bigger_is_better'] = False
            yaml_schema['metrics'].sort(key=lambda x: x['name'])
            yaml_schema['run_fields'].sort(key=lambda x: x['name'])
            yaml_schema['machine_fields'].sort(key=lambda x: x['name'])
        self.assertEqual(rest_schema, yaml_schema)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0], ])