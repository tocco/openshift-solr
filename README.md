# Solr on Openshift
[![Build Status](https://travis-ci.org/pgerber/openshift-solr.svg?branch=master)](https://travis-ci.org/pgerber/openshift-solr)

This image is set up to provide search functionality to the [Tocco Business Framework](https://www.tocco.ch). It has been optimized
to run on the [OpenShift platform](https://www.openshift.com) provided by [VSHN](https://vshn.ch/en/).

## Caveats

### Timezone

Solr fails to start if the timezone on the Gluster Cluster differs. Apparently, the locking mechanism inherited from Lucene wrongfully
believes that the lock file has been modified. To resolve the issue the timezone is now explicitly set to `Europe/Zurich`

See also:
* https://bugzilla.redhat.com/show_bug.cgi?id=1430659
* https://discuss.elastic.co/t/es-cluster-in-docker-containers-alreadyclosedexception-underlying-file-changed-by-an-external-force/48874

### .trashcan

In our Openshift environment a persistent volume is mounted from a Gluster cluster. The mount contains a `.trashcan` directory
and Solr won't have access to it. Unfortunately, Solr can't deal with that. To get it working anyway, the volume is mounted
at `/persist` and the data directory is a subdirectory of it (`/persist/index_data`). This way `.trashcan` (`/persist/.trashcan`) is no longer
in Solr's data directory.
