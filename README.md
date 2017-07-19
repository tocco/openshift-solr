# Solr on Openshift
[![Build Status](https://travis-ci.org/pgerber/openshift-solr.svg?branch=master)](https://travis-ci.org/pgerber/openshift-solr)

This image is set up to provide search functionality to the [Tocco Business Framework](https://www.tocco.ch). It has been optimized
to run on the [OpenShift platform](https://www.openshift.com) provided by [VSHN](https://vshn.ch/en/).

## Caveats

### .trashcan

In our Openshift environment a persistent volume is mounted from a Gluster cluster. The mount contains a `.trashcan` directory
and Solr won't have access to it. Unfortunately, Solr can't deal with that. To get it working anyway, the volume is mounted
at `/persist` and the data directory is a subdirectory of it (`/persist/index_data`). This way `.trashcan` (`/persist/.trashcan`) is no longer
in Solr's data directory.

### Lock File Removal

The lock file is currently removed during startup to avoid already-locked errors.
