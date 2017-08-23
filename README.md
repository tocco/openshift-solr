# Solr on Openshift
[![Build Status](https://travis-ci.org/tocco/openshift-solr.svg?branch=master)](https://travis-ci.org/tocco/openshift-solr)

This image is set up to provide search functionality to the [Tocco Business Framework](https://www.tocco.ch). It has been optimized
to run on the [OpenShift platform](https://www.openshift.com) provided by [VSHN](https://vshn.ch/en/).

## Configuration

All configuration parameters available in /opt/solr/bin/solr.in.sh within the image can be overridden using environment variables by
prefixing `SOLR_`.

### Example

Change parameter `SOLR_HEAP=1024m`:

```
SOLR_SOLR_HEAP=1024m
```

Take a look at the [sample config](tests/sample_config.conf) used in the tests to see available properties.

## Caveats

### .trashcan

In our Openshift environment a persistent volume is mounted from a Gluster cluster. The mount contains a `.trashcan` directory
and Solr won't have access to it. Unfortunately, Solr can't deal with that. To get it working anyway, the volume is mounted
at `/persist` and the data directory is a subdirectory of it (`/persist/index_data`). This way `.trashcan` (`/persist/.trashcan`) is no longer
in Solr's data directory.

### Lock File Removal

The lock file is currently removed during startup to avoid already-locked errors.
