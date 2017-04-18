#!/usr/bin/python3
from SolrClient import SolrClient

client = SolrClient('http://localhost:8983/solr/')
assert client.index('nice2_index', [
    {
        'id': 'no_1',
        'pk': '1',
        'entity_type': 'auxilary',
        'entity_version': 1,
        'index_priority': 0,
        'business_unit': 'bu1',
        'text_en': 'some sample text'
    },
]), "failed to insert entry"
client.commit('nice2_index', softCommit=True)
result = client.query('nice2_index', {'q': 'text_en:"some sample text"'})
result_count = result.get_results_count()
assert result_count == 1, "indexed text not found (result count: {})".format(result_count)
