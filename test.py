#!/usr/bin/python3
from SolrClient import SolrClient
import os
import requests
import subprocess
import tempfile
import time


class Docker:
    def __init__(self):
        self.volume = tempfile.TemporaryDirectory()

    def __del__(self):
        if hasattr(self, 'volume'):
           self.volume.cleanup()

    def __enter__(self):
        self._start_docker()
        return SolrClient('http://localhost:8983/solr/')

    def __exit__(self, exc_type, exc_value, traceback):
        print('terminating Solr')
        self.proc.terminate()
        self.proc.wait()
        print('Solr terminated')

    def _start_docker(self):
        print('Starting Solr')
        self.proc = subprocess.Popen(['docker', 'run', '-u', '{}:0'.format(os.getuid()), '-p', '8983:8983', '-v', self.volume.name + ':/persist', 'solr_image'])

        while True:
            time.sleep(1)
            try:
                resp = requests.get('http://localhost:8983/solr/nice2_index/update?commit=true&wt=json')
                if resp.status_code != 200:
                    print('waiting for Solr … (status code: {})'.format(resp.status_code))
                    continue
                break
            except requests.exceptions.ConnectionError:
                print('waiting for Solr … (cannot connect)')

            try:
                self.proc.wait(timeout=0)
                raise AssertionError('Solr container died')
            except subprocess.TimeoutExpired:
                pass


def find_some_sample_text(client):
    result = client.query('nice2_index', {'q': 'text_en:"some sample text"'})
    assert result.get_results_count() == 1, "unexpected result count ({})".format(result.get_results_count())
    assert result.get_field_values_as_list('id') == ['no_1']
    assert result.get_field_values_as_list('business_unit') == ['bu1']
    assert result.get_field_values_as_list('entity_type') == ['auxiliary']


def main():
    docker = Docker()

    with docker as client:
        assert client.index('nice2_index', [
            {
                'id': 'no_1',
                'pk': '1',
                'entity_type': 'auxiliary',
                'entity_version': 1,
                'index_priority': 0,
                'business_unit': 'bu1',
                'text_en': 'some sample text'
            },
        ]), "failed to insert entry"
        client.commit('nice2_index', softCommit=True)
        find_some_sample_text(client)

    # Restart Solr to see if persistent volume contains all information needed
    # to continue regular operations.
    with docker as client:
        find_some_sample_text(client)


if __name__ == '__main__':
    main()
